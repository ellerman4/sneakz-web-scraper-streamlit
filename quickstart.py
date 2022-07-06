
import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from charts import draw_pie
import Converter


st.title("Sneakz web scraper")
st.write("Results")

with st.sidebar:
    text_input = st.text_input(label='Enter your Steam ID')
    submit_button = st.button(label='Scrape')
    st.caption('Enter any form of steam id')

if not submit_button:
    st.stop()

driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\chromedriver')
s_id = Converter.to_steamID(text_input)
driver.get(f"https://snksrv.com/surfstats/?view=profile&id={s_id}")

# Define each column in the third table via xpath
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

#Create dataframe from the result list and build a table schema
df = pd.DataFrame(result)
table_col, chart_col = st.columns(2)

with table_col:
    st.dataframe(df, height = 405, width = 700)


driver.close()

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

st.download_button(
    "Press to Download",
    csv,
    "file.csv",
    "text/csv",
    key='download-csv'
)

with chart_col:
    draw_pie(df)

metcol1, metcol2 = st.columns(2)

with metcol1:
    st.metric(label="Maps Completed", value=df.shape[0])

maps_left = 944- df.shape[0]

with metcol2:
    st.metric(label="Maps Unfinished", value=maps_left)
