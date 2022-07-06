
from streamlit_echarts import st_echarts
from st_aggrid import AgGrid, GridOptionsBuilder

def draw_pie(df):
    options = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center"},
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
        options=options, height="500px",
    )


def draw_table(df):
    custom_css = {
    ".trade-buy-green": {"color": "green !important"},
    ".trade-sell-red": {"color": "red !important"},
    }

    AgGrid(df, theme="streamlit", custom_css=custom_css)