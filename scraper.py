
import streamlit as st
import pandas as pd
from streamlit_player import st_player
from selenium import webdriver
from selenium.webdriver.common.by import By
from bokeh.plotting import figure
from streamlit_echarts import st_echarts
from quickstart import df

options = {
    "tooltip": {"trigger": "item"},
    "legend": {"top": "5%", "left": "center"},
    "series": [
        {
            "name": "访问来源",
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {
                "borderRadius": 10,
                "borderColor": "#fff",
                "borderWidth": 2,
            },
            "label": {"show": False, "position": "center"},
            "emphasis": {
                "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
            },
            "labelLine": {"show": False},
            "data": [
                {"value": df.shape[0], "name": "Maps Completed"},
                {"value": 944, "name": "Total Maps"},
            ],
        }
    ],
}
st_echarts(
    options=options, height="500px",
)