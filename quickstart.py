import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from charts import draw_pie, draw_table, draw_bar, draw_flag, players_bar, draw_rank, draw_current_rank, draw_bonus_pie
import Converter
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
from css.custom_css import button_css, download_button_css
import psycopg2
from datetime import datetime
import timeit
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


# Create a runtime error if user enters an invalid SteamID
invalid_id = RuntimeError('You may have entered an invalid SteamID')

st.set_page_config(layout="wide")

options = Options()
options.add_argument("--headless")

# Cache geckodriver service to not install on every visit
@st.cache(allow_output_mutation=True)
def set_service():
    service = Service(GeckoDriverManager().install())
    return service


# Initialize connection to database
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

# Create a cursor to interact with the database
conn = init_connection()
cur = conn.cursor()

# Load some custom css
#download_button_css()
button_css()


# Fix padding
st.markdown('''
    <style>
    .css-18e3th9 {
        padding: 0rem 1rem 10rem;
        flex: 1 1 0%;
        width: 100%;
        padding-left: 5rem;
        padding-right: 5rem;
        min-width: auto;
        max-width: initial;
        top: 15px;
    }
    </style>''',
    unsafe_allow_html=True
    )


# Build a sidebar for user input
with st.sidebar:
    #card()
    st.title("Sneakz web scraper")
    text_input = st.text_input(label='Enter your Steam ID').strip()
    submit_button = st.button(label='Scrape')
    st.subheader('SteamID Examples:')
    st.info('''Legacy SteamID: STEAM_1:1:171196293
                SteamID64: 76561198302658315
                SteamID3: [U:1:342392587]''')

# Stops the entire process until submit_button is clicked
if not submit_button:
    st.stop()

# Start a timer to log scrape time
start = timeit.default_timer()


# Initialize streamlit spinner animation while scraping data
with st.spinner('Retrieving Surf Stats...'):
    try:
        s_id = Converter.to_steamID(text_input)
        id64 = Converter.to_steamID64(text_input)
    except:
        st.exception(invalid_id)
        st.stop()
    
    driver = webdriver.Firefox(options=options, service=set_service())
    driver.get(f"https://snksrv.com/surfstats/?view=profile&id={s_id}")

    # Get general player data
    player_name = driver.find_element(By.XPATH, '//h2/a').text
    points = driver.find_element(By.XPATH, '//table/tbody/tr/td').text[8:]
    player_country = driver.find_element(By.XPATH, '//table/tbody/tr/td[2]').text[9:]
    player_rank = driver.find_element(By.XPATH, '//b').text[6:]
    bonus_completion = driver.find_element(By.XPATH, '//table/tbody/tr[3]/td').text[19:]

    # Get player record data
    map_records = driver.find_element(By.XPATH, '//tbody/tr[2]/td[2]').text[13:]
    bonus_records = driver.find_element(By.XPATH, '//tbody/tr[3]/td[2]').text[15:]
    stage_records = driver.find_element(By.XPATH, '//tbody/tr[4]/td[2]').text[15:]

    # Get player map time data
    map_names = driver.find_elements(By.XPATH, '//table[3]/tbody/tr/td/a')
    rank = driver.find_elements(By.XPATH, '//table[3]/tbody/tr/td[2]')
    pb = driver.find_elements(By.XPATH, '//table[3]/tbody/tr/td[3]')
    date = driver.find_elements(By.XPATH, '//table[3]/tbody/tr/td[4]')
    start_speed = driver.find_elements(By.XPATH, '//table[3]/tbody/tr/td[5]')

    result = [] # Blank list to be appended later

    # Iterate through all rows in the table, getting values for all rows
    for i,v in enumerate(map_names):
        temp_data = {'Map Name': map_names[i].text,
                    'Rank': rank[i].text,
                    'Personal Best': pb[i].text,
                    'Date': date[i].text,
                    'Start Speed': start_speed[i].text}
        result.append(temp_data)

    driver.close()

# Stop the timer and calculate execution time
stop = timeit.default_timer()
execution_time = stop - start


# Delete row by steamid if exists
cur.execute("DELETE FROM player_stats WHERE steamid = %s",(s_id,))

# Insert player stats into database
cur.execute("""INSERT INTO player_stats(name, steamid, points, map_records, date, rank, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (player_name, s_id, points, map_records, datetime.today(), player_rank, player_country))

# Commit database changes
conn.commit()


#Create dataframe from the result list
df = pd.DataFrame(result)
df['Rank'] = pd.to_numeric(df['Rank'])  # Convert rank column to numeric for accurate sorting/filtering

# Read maps.csv with map name and map tier data
maps_df = pd.read_csv('./data/maps.csv')

# Merge player stats with map tier on Map Name column
df = pd.merge(df, maps_df, on='Map Name')


# Start building the dashboard when scraping is complete
draw_flag(player_name, player_country, id64)


if int(player_rank) <= 100:
    st.markdown(f"Rank:  {player_rank}  ⚡")
else:
    st.markdown(f"Rank:  {player_rank}")

# Create columns for records
map_col, bonus_col, stage_col= st.columns(3)

# Include tooltip info for records via inline html
with map_col:
    draw_current_rank(points)

with bonus_col:
    draw_rank(points)

with stage_col:
    st.markdown(f'''<div class="tooltip",
                    style="cursor:pointer;
                            margin-left: -877px;
                            margin-top: 71px;",
                    title="Records">🥇{map_records} 🥈{bonus_records} 🥉{stage_records}</div>''',
                unsafe_allow_html=True)


# Create a column layout table and bar chart
table_col, chart_col = st.columns(2)

# Create a column for pie charts
pie_col1, pie_col2 = st.columns(2)

# Convert dataframe to csv
@st.cache(ttl=300, max_entries=2)
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

# Draw table and download button in table column
with table_col:
    st.download_button("Press to Download", csv, "file.csv", "text/csv", key='download-csv')
    draw_table(df)

with chart_col:
    draw_bar(df)


# Pie charts in dedicated columns under table/bar chart columns
with pie_col1:
    draw_pie(df)

with pie_col2:
    draw_bonus_pie(bonus_completion)


# Display top 25 players bar chart under a markdown
st.markdown('***')
players_bar()

@st.cache(allow_output_mutation=True, ttl=300, max_entries=2)
def gen_profile_report(df, *report_args, **report_kwargs):
    return df.profile_report(*report_args, **report_kwargs)


# Create a profile report
pr = gen_profile_report(df)

# Create expander for pandas profile report
with st.expander("See Pandas Profile Report"):
    st_profile_report(pr, key='profile-report')
    export=pr.to_html()
    st.download_button(label="Download Full Report", data=export, file_name='report.html')

# Write execution time
st.write(execution_time)