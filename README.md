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

![web-scraper-preview](https://user-images.githubusercontent.com/106990217/177654478-67fe69d3-16c9-4590-b44e-4acb144ece50.png)

Once the scraping process is done an interactive table will be generated with the option to export as a .csv file.

## Acknowledgements
[Converter](https://github.com/AlexHodgson/steamid-converter) script provided by [Alex Hodgson](https://github.com/AlexHodgson)
