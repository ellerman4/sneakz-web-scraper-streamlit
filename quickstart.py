import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from charts import draw_pie, draw_table, draw_bar, draw_line
import Converter
from st_aggrid import AgGrid

st.set_page_config(layout="wide")

# STEAM_1:1:56970041

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

with st.spinner('Retrieving Surf Stats...'):
    # Get link, with provided SteamID
    driver = webdriver.Chrome(executable_path='chromedriver')
    s_id = Converter.to_steamID(text_input)
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

    # Get player completion data
    map_records = driver.find_element(By.XPATH, '//tbody/tr[2]/td[2]').text

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

maps_df = pd.read_csv('maps.csv')       # Read maps.csv with map name and map tier data

df = pd.merge(df, maps_df, on='Map Name')   # Merge player stats with map tier on Map Name column


# Start building the dashboard when scraping is complete
st.title(f"{player_name}'s surf stats")

if int(player_rank) <= 100:
    st.markdown(f"Rank:  {player_rank}  ⚡")
else:
    st.markdown(f"Rank:  {player_rank}")

st.markdown(f'Points:  {points} ⬆')

st.markdown(f'Map Records:  {map_records} 🥇')

table_col, chart_col = st.columns(2)

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

with table_col:
    st.download_button("Press to Download", csv, "file.csv", "text/csv", key='download-csv')
    draw_table(df)
    draw_line(df)

with chart_col:
    draw_bar(df)
    draw_pie(df)


