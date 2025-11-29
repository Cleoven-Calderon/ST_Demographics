import pandas as pd
import streamlit as st
import requests
import altair as alt
from functools import reduce


url = "https://api.worldbank.org/v2/country?format=json&per_page=500"
resp = requests.get(url).json()
countries = {c["name"]: c["id"] for c in resp[1] if c["region"]["value"] != "Aggregates"}



st.set_page_config(
    layout="wide",
    page_title="Data Dashboard",
    page_icon=":bar_chart:"
)


st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Configuration")
    st.markdown("---")
    country_names = sorted(countries.keys())
    country_name = st.selectbox(
        "Select a country",
        options=list(countries.keys()),
        index=list(countries.keys()).index("Philippines")  # default selected
    )

    # Get the corresponding country code
    country_code = countries[country_name]
    if st.button("Refresh Data"):
        st.cache_data.clear()
country_caps = country_name.upper()
st.title(f"{country_caps} DEMOGRAPHICS PREVIEW")
st.markdown("_Early Prototype v0.1.1_")
st.markdown("---")

indicators = {
    "GDP": "NY.GDP.MKTP.CD",
    "GDP per capita": "NY.GDP.PCAP.CD",
    "Population": "SP.POP.TOTL",
    "Inflation": "FP.CPI.TOTL.ZG"
}

dfs = []

for name, code in indicators.items():
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{code}?format=json&per_page=200"
    response = requests.get(url).json()
    data = response[1]

    temp_df = pd.DataFrame([
        {"year": int(item["date"]), name: item["value"]}
        for item in data
    ])
    dfs.append(temp_df)
df = reduce(lambda left, right: pd.merge(left, right, on="year"), dfs)

df_reset = df.reset_index()
df_reset["year"] = df_reset["year"].astype(str)
df_reset["GDP (Billion USD)"] = df_reset["GDP"] / 1_000_000_000
df_reset["Population (Million)"] = df_reset["Population"] / 1_000_000
plot_df = df_reset[["year", "GDP (Billion USD)", "GDP per capita", "Population (Million)", "Inflation"]]
plot_df = plot_df.melt(id_vars="year", var_name="Indicator", value_name="Value")

chart = alt.Chart(plot_df).mark_line(point=True).encode(
    x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("Value:Q", title="Value"),
    color="Indicator:N",
    tooltip=["year", "Indicator", "Value"]
).properties(width=800, height=400).interactive()


st.altair_chart(chart, use_container_width=True)

with st.expander("More Insights"):
    # GDP CHART
    gdp_df = plot_df[plot_df["Indicator"] == "GDP (Billion USD)"]
    st.subheader("GDP (Billion USD)")

    gdp_chart = (
        alt.Chart(gdp_df)
        .mark_line(point=False, color="#83c9ff")
        .encode(
            x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Value:Q", title="GDP (Billion USD)"),
            tooltip=["year", "Value"]
        )
        .properties(width=800, height=400)
        .interactive()
    )
    st.altair_chart(gdp_chart, use_container_width=True)

    # PER CAPITA CHART
    per_capita_df = plot_df[plot_df["Indicator"] == "GDP per capita"]
    st.subheader("GDP per capita")

    per_capita_chart = (
        alt.Chart(per_capita_df)
        .mark_area(point=False, color="#0068c9")
        .encode(
            x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Value:Q", title="GDP per capita"),
            tooltip=["year", "Value"]
        )
        .properties(width=800, height=400)
        .interactive()
    )
    st.altair_chart(per_capita_chart, use_container_width=True)

    # INFLATION CHART
    inflation_df = plot_df[plot_df["Indicator"] == "Inflation"]
    st.subheader("Inflation (Annual %)")

    inflation_chart = (
        alt.Chart(inflation_df)
        .mark_line(point=True, color="#ffabab")
        .encode(
            x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Value:Q", title="Inflation (%)"),
            tooltip=["year", "Value"]
        )
        .properties(width=800, height=400)
        .interactive()
    )
    st.altair_chart(inflation_chart, use_container_width=True)

    # POPULATION CHART
    population_df = plot_df[plot_df["Indicator"] == "Population (Million)"]
    st.subheader("Population (Million)")

    population_chart = (
        alt.Chart(population_df)
        .mark_bar(point=False, color="#ff2b2b")
        .encode(
            x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Value:Q", title="Population (Million)"),
            tooltip=["year", "Value"]
        )
        .properties(width=800, height=400)
        .interactive()
    )
    st.altair_chart(population_chart, use_container_width=True)
