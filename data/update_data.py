from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def update_maps():
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(f"https://snksrv.com/surfstats/?view=maps")

    map_name = driver.find_elements(By.XPATH, '//table/tbody/tr/td[1]/a')
    map_tier = driver.find_elements(By.XPATH, '//table/tbody/tr/td[2]')

    result = []
    
    # Loop through the elements and append result list
    for i,v in enumerate(map_name):
        temp_data = {'Map Name': map_name[i].text,
                    'Map Tier': map_tier[i].text}
        result.append(temp_data)

    driver.close()

    #Create a datafrane from the result
    df = pd.DataFrame(result)

    # convert Map Tier column to numberic for proper filtering
    df['Map Tier'] = pd.to_numeric(df['Map Tier'])

    # Drop invalid and null Map Tier values
    clean_df = df.drop(df[df['Map Tier'] > 7 ].index).dropna()
    data = clean_df.astype({'Map Tier':'int'})

    # Save the data
    data.to_csv('./data/maps.csv', index = False)



def top_players():
    driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\chromedriver')
    driver.get(f"https://snksrv.com/surfstats/?view=players")

    player_name = driver.find_elements(By.XPATH, '//table/tbody/tr/td/a')
    player_country = driver.find_elements(By.XPATH, '//table/tbody/tr/td[2]')
    player_points = driver.find_elements(By.XPATH, '//table/tbody/tr/td[3]')
    maps_completed = driver.find_elements(By.XPATH, '//table/tbody/tr/td[4]')


    result = [] # Blank list to be appended later

    # Iterate through all rows in the table, getting values for all rows
    for i,v in enumerate(player_name):
        temp_data = {'Player Name': player_name[i].text,
                    'Player Country': player_country[i].text,
                    'Points': player_points[i].text,
                    'Maps Completed': maps_completed[i].text}
        result.append(temp_data)

    driver.close()

    #Create dataframe from the result list
    df = pd.DataFrame(result)
    df = df.iloc[: , 0:]
    df.to_csv('./data/top_players.csv', index = False)
