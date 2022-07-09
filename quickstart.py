import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from charts import draw_pie, draw_table, draw_bar, draw_flag, players_bar, draw_rank
import Converter
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

# Create a runtime error if user enters an invalid SteamID
invalid_id = RuntimeError('You may have entered an invalid SteamID')

st.set_page_config(layout="wide")

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

if int(player_rank) <= 100:
    st.markdown(f"Rank:  {player_rank}  ⚡")
else:
    st.markdown(f"Rank:  {player_rank}")

st.markdown(f'Points:  {points} ⬆')

# Create columns for records
map_col, bonus_col, stage_col= st.columns(3)

# Include tooltip info for records via inline html
with map_col:
    st.markdown(f'<div class="tooltip", style="cursor:pointer;", title="Map Records">🥇{map_records}</div>', unsafe_allow_html=True)
    #draw_rank(points)

with bonus_col:
    st.markdown(f'<div class="tooltip", style="cursor:pointer; margin-left: -436px;", title="Bonus Records">🥈{bonus_records}</div>', unsafe_allow_html=True)

with stage_col:
    st.markdown(f'<div class="tooltip", style="cursor:pointer; margin-left: -864px;", title="Stage Records">🥉{stage_records}</div>', unsafe_allow_html=True)


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
