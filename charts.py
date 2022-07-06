import pandas as pd
import plotly.express as px
maps = 944
map_count =555

test = {'Maps Completed': maps,
        'Maps Unfinished': map_count}

map_df = pd.DataFrame(test, index=[0])
print(map_df)


fig = px.bar(map_df, x="Maps Completed", y="Maps Unfinished")
fig.show()