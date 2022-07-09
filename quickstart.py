import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from charts import draw_pie, draw_table, draw_bar, draw_flag, players_bar, draw_rank, draw_current_rank
import Converter
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

# Create a runtime error if user enters an invalid SteamID
invalid_id = RuntimeError('You may have entered an invalid SteamID')

st.set_page_config(layout="wide")

st.markdown(
"""
<style>
.css-wq85zr {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.25rem;
    margin: 0px;
    border-radius: 10px;
    line-height: 1.6;
    color: inherit;
    width: auto;
    user-select: none;
    background-color: rgb(43, 44, 54);
    border: 1px solid rgba(250, 250, 250, 0.2);
    width: 304px;
}
.css-wq85zr:before {
    content: '';
    background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
    position: absolute;
    top: -2px;
    left:-2px;
    background-size: 400%;
    z-index: -1;
    filter: blur(5px);
    width: calc(100% + 4px);
    height: calc(100% + 4px);
    animation: glowing 20s linear infinite;
    opacity: 0;
    transition: opacity .3s ease-in-out;
    border-radius: 10px;
}
.css-wq85zr:active {
    color: #000
}
.css-wq85zr:active:after {
    background: transparent;
}
.css-wq85zr:hover:before {
    opacity: 1;
}

.css-wq85zr:after {
    z-index: -1;
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background: #111;
    left: 0;
    top: 0;
    border-radius: 10px;
}

@keyframes glowing {
    0% { background-position: 0 0; }
    50% { background-position: 400% 0; }
    100% { background-position: 0 0; }
}
</style>
""",
unsafe_allow_html=True
)

# Build a sidebar for user input
with st.sidebar:
    st.title("Sneakz web scraper")
    text_input = st.text_input(label='Enter your Steam ID').strip()
    submit_button = st.button(label='Scrape')
    st.subheader('SteamID Examples:')
    st.markdown('Legacy SteamID: STEAM_1:1:171196293')
    st.markdown('SteamID64: 76561198302658315')
    st.markdown('SteamID3: [U:1:342392587]')

# Stops the entire process until submit_button is clicked
if not submit_button:
    st.stop()

# Initialize streamlit spinner animation while scraping data
with st.spinner('Retrieving Surf Stats...'):
    try:
        s_id = Converter.to_steamID(text_input)
    except:
        st.exception(invalid_id)
        st.stop()
    
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(f"https://snksrv.com/surfstats/?view=profile&id={s_id}")

    # Get general player data
    player_name = driver.find_element(By.XPATH, '//h2/a').text
    points = driver.find_element(By.XPATH, '//table/tbody/tr/td').text.strip('Points: ')
    player_country = driver.find_element(By.XPATH, '//table/tbody/tr/td[2]').text.strip('Country: ')
    player_rank = driver.find_element(By.XPATH, '//b').text.strip('Rank: ')

    # Get player record data
    map_records = driver.find_element(By.XPATH, '//tbody/tr[2]/td[2]').text.strip('Map Records: ')
    bonus_records = driver.find_element(By.XPATH, '//tbody/tr[3]/td[2]').text.strip('Bonus Records: ')
    stage_records = driver.find_element(By.XPATH, '//tbody/tr[4]/td[2]').text.strip('Stage Records: ')

    # Get player map time data
    map_names = driver.find_elements(By.XPATH, '//table[3]/tbody/tr/td/a')
    rank = driver.find_elements(By.XPATH, '//table[3]/tbody/tr/td[2]')
    pb = driver.find_elements(By.XPATH, '//table[3]/tbody/tr/td[3]')
    date = driver.find_elements(By.XPATH, '//table[3]/tbody/tr/td[4]')
    start_speed = driver.find_elements(By.XPATH, '//table[3]/tbody/tr/td[5]')

    result = [] # Blank list to be appended later

    # Iterate through all rows in the table, getting values for all rows
    for i in range(len(map_names)):
        temp_data = {'Map Name': map_names[i].text,
                    'Rank': rank[i].text,
                    'Personal Best': pb[i].text,
                    'Date': date[i].text,
                    'Start Speed': start_speed[i].text}
        result.append(temp_data)

    driver.close()

#Create dataframe from the result list
df = pd.DataFrame(result)
df['Rank'] = pd.to_numeric(df['Rank'])  # Convert rank column to numeric for accurate sorting/filtering

# Read maps.csv with map name and map tier data
maps_df = pd.read_csv('https://raw.githubusercontent.com/ellerman4/timed-scraper/master/data/maps.csv')

# Merge player stats with map tier on Map Name column, drop unnamed index column
df = pd.merge(df, maps_df, on='Map Name')

# Start building the dashboard when scraping is complete
draw_flag(player_name, player_country, s_id)

# 
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
                    title="Stage Records">🥇{map_records} 🥈{bonus_records} 🥉{stage_records}</div>''',
                unsafe_allow_html=True)


# Create a column layout for plots
table_col, chart_col = st.columns(2)

# Convert dataframe to csv
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

with table_col:
    st.download_button("Press to Download", csv, "file.csv", "text/csv", key='download-csv')
    draw_table(df)
    players_bar()

with chart_col:
    draw_bar(df)
    draw_pie(df)

# Create a profile report
pr = df.profile_report()

# Create expander for pandas profile report
with st.expander("See Pandas Profile Report"):
    st_profile_report(pr, key='profile-report')
    export=pr.to_html()
    st.download_button(label="Download Full Report", data=export, file_name='report.html')
