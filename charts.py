
from streamlit_echarts import st_echarts
from st_aggrid import AgGrid
import numpy as np

def draw_pie(df):
    options = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "0%", "left": "center"},
        "series": [
            {
                "name": "maps_pie",
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
                    {"value": (944 - df.shape[0]), "name": "Maps Left"},
                ],
            }
        ],
    }
    st_echarts(
        options=options, height="475px",
    )


def draw_table(df):
    custom_css = {
    '.ag-header-cell-label': {'justify-content': 'center'},
    '.ag-theme-streamlit .ag-root-wrapper': {'text-align': 'center'}
    }
    AgGrid(df, theme="streamlit", custom_css=custom_css)


def draw_bar(df):
    # Assign count of Map Tiers to respective variables
    tier1, tier2 = np.sum(df['Map Tier'] == 1), np.sum(df['Map Tier'] == 2)
    tier3, tier4 = np.sum(df['Map Tier'] == 3), np.sum(df['Map Tier'] == 4)
    tier5, tier6 = np.sum(df['Map Tier'] == 5), np.sum(df['Map Tier'] == 6)
    
    options = {
    "legend": {"top": "0%", "left": "center"},
    "xAxis": {
        "type": "category",
        "data": ["Tier 1", "Tier 2", "Tier 3", "Tier 4", "Tier 5", "Tier 6"],
    },
    "yAxis": {"type": "value"},
    "series": [{"data": [int(tier1), int(tier2), int(tier3), int(tier4), int(tier5), int(tier6)], "type": "bar"}],  # Echarts cant understand np64 integers, convert to regular int
    }
    st_echarts(options=options, height="450px")
