# Overview
Browser based web scraper for scraping [Sneakz](https://snksrv.com/surfstats/) surf data for a specified user.  
Results are returned in a table with the option to download as csv.  
Steam ID can be any type of steam id, as it converts to a legacy steam id.  

- Streamlit
```python
pip install Streamlit
```
- Pandas
```python
pip install Pandas
```
- Selenium
```python
pip install Selenium
```


## Usage
Initialize a local Streamlit server with the command:
```python
streamlit run quickserve.py
```
Navigate to the provided link and enter your steam id

Note: Any form of steam id will work, as it is converted to a legacy steam id.  

The included chrome driver will open and start scraping, this can take up to a minute.

Once the scraping process is done an interactive table will be generated with the option to export as a .csv file.

![f2fe1f2ad68e0e1cfedfd5ac05a4e802](https://user-images.githubusercontent.com/106990217/178086877-c6e54b5b-ff3c-402f-8012-186a9708641a.png)


You can also review the results in an auto-generated Pandas Profile.  

![e41bff85ebea34dc59bb8a30af7850ff](https://user-images.githubusercontent.com/106990217/177888908-6cecaf64-63cf-4e38-8e8f-eeeab88df6b5.png)

![724de7daa95f984bc094ae971e6b4630](https://user-images.githubusercontent.com/106990217/177889028-349fd800-5ae2-4bef-80ea-1d4642070f32.png)


## Acknowledgements
[Converter](https://github.com/AlexHodgson/steamid-converter) script provided by [Alex Hodgson](https://github.com/AlexHodgson)
