import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

st.set_page_config(page_title="Indian Startup Funding Map", layout="wide")
@st.cache_data
def load_data():
    geojson = gpd.read_file("india_state.geojson")

    count_2024 = pd.read_csv("count_2024.csv")
    count_2025 = pd.read_csv("count_2025.csv")

    # Standardize names for both datasets
    mapping = {
        "Odisha": "Orissa",
        "Uttarakhand": "Uttaranchal",
        "Telangana": "Andhra Pradesh",
    }
    count_2024["State"] = count_2024["State"].replace(mapping)
    count_2025["State"] = count_2025["State"].replace(mapping)

    count_2024["Year"] = 2024
    count_2025["Year"] = 2025

    df = pd.concat([count_2024, count_2025], ignore_index=True)
    return geojson, df

geojson, df = load_data()

# ---- Title ----
st.title("Indian Startup Growth Over Time (2024–2025)")
st.write(
    "This interactive choropleth map visualizes the number of startups emerging from each Indian state, "
    "based on funding data collected from **Startuptalky (2024–2025)**."
)
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="State",
    featureidkey="properties.NAME_1",
    color="Startup_count",
    color_continuous_scale="Greens",
    hover_name="State",
    animation_frame="Year",  # <-- Magic here!
    title="Startup Count by Indian State (Animated by Year)",
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    margin={"r":0,"t":30,"l":0,"b":0},
    title_x=0.5,
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")
st.markdown("**Built by Aniket Dash** | Data Source: Startuptalky (2024 & 2025)")