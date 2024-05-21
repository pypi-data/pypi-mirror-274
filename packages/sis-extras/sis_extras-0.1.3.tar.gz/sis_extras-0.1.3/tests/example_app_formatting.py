import altair as alt
import pandas as pd
from sis_extras.formatting import tile

# Sample DataFrame
data = pd.DataFrame({"x": range(10), "y": range(10)})

# Sample Chart
chart = alt.Chart(data).mark_line().encode(x="x", y="y")

# Create a tile with data and chart
tile(data, "Sample Tile", chart=chart, sql="SELECT x, y FROM your_table")
