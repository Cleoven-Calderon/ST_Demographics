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
st.title(f"{country_caps} | Economic & Demographic Indicators")
st.markdown("_Early Prototype v0.1.2_")
st.markdown("---")

indicators = {
    "GDP": "NY.GDP.MKTP.CD",
    "GDP per capita": "NY.GDP.PCAP.CD",
    "Inflation": "FP.CPI.TOTL.ZG",

    "Population": "SP.POP.TOTL",
    "Life Expectancy": "SP.DYN.LE00.IN",
    "Fertility Rate": "SP.DYN.TFRT.IN"
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
plot_df = df_reset[["year", "GDP (Billion USD)", "GDP per capita", "Population (Million)",
                    "Inflation", "Life Expectancy", "Fertility Rate"]]
plot_df = plot_df.melt(id_vars="year", var_name="Indicator", value_name="Value")

chart = alt.Chart(plot_df).mark_line(point=True).encode(
    x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("Value:Q", title="Value"),
    color="Indicator:N",
    tooltip=["year", "Indicator", "Value"]
).properties(width=800, height=400).interactive()


st.altair_chart(chart, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    with st.expander("Economy"):
        # GDP CHART
        gdp_df = plot_df[plot_df["Indicator"] == "GDP (Billion USD)"]
        st.subheader("GDP (Billion USD)")
        latest_year_gdp = gdp_df[gdp_df["Value"].notnull()]["year"].max()
        current_gdp = gdp_df[gdp_df["year"] == latest_year_gdp]["Value"].values[0]
        st.write(f"Current GDP Value {latest_year_gdp}: {round(current_gdp, 2)} Billion")
        gdp_chart = (
            alt.Chart(gdp_df)
            .mark_line(point=False, color="#ff6b6b")
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
        st.subheader("GDP Per Capita")
        latest_year_pc = per_capita_df[per_capita_df["Value"].notnull()]["year"].max()
        current_gdp_pc = per_capita_df[per_capita_df["year"] == latest_year_pc]["Value"].values[0]
        st.write(f"Current GDP Per Capita Value {latest_year_pc}: {round(current_gdp_pc, 2)} US Dollars")
        per_capita_chart = (
            alt.Chart(per_capita_df)
            .mark_area(point=False, color="#ff0000")
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
        latest_year_inf = inflation_df[inflation_df["Value"].notnull()]["year"].max()
        current_inflation = inflation_df[inflation_df["year"] == latest_year_pc]["Value"].values[0]
        st.write(f"Current Inflation Rate {latest_year_inf}: {round(current_inflation, 2)}%")
        inflation_chart = (
            alt.Chart(inflation_df)
            .mark_line(point=True, color="#ff6b6b")
            .encode(
                x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Value:Q", title="Inflation (%)"),
                tooltip=["year", "Value"]
            )
            .properties(width=800, height=400)
            .interactive()
        )
        st.altair_chart(inflation_chart, use_container_width=True)


with col2:
    with st.expander("Demographics"):

        # POPULATION CHART
        population_df = plot_df[plot_df["Indicator"] == "Population (Million)"]
        st.subheader("Population (Million)")
        latest_year = population_df["year"].max()
        current_population = population_df[population_df["year"] == latest_year]["Value"].values[0]
        st.write(f"Current Population ({latest_year}): {round(current_population)} Million")
        population_chart = (
            alt.Chart(population_df)
            .mark_bar(point=False, color="#66ff66")
            .encode(
                x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Value:Q", title="Population (Million)"),
                tooltip=["year", "Value"]
            )
            .properties(width=800, height=400)
            .interactive()
        )
        st.altair_chart(population_chart, use_container_width=True)

        # LIFE EXPECTANCY CHART
        life_expectancy_df = plot_df[plot_df["Indicator"] == "Life Expectancy"]
        st.subheader("Life Expectancy")
        latest_year_le = life_expectancy_df[life_expectancy_df["Value"].notnull()]["year"].max()
        current_life_expectancy = life_expectancy_df[life_expectancy_df["year"] == latest_year_le]["Value"].values[0]
        st.write(f"Current Life Expectancy ({latest_year_le}): {round(current_life_expectancy, 2)} Years")
        life_expectancy_chart = (
            alt.Chart(life_expectancy_df)
            .mark_bar(point=False, color="#99ff99")
            .encode(
                x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Value:Q", title="Life Expectancy"),
                tooltip=["year", "Value"]
            )
            .properties(width=800, height=400)
            .interactive()
        )
        st.altair_chart(life_expectancy_chart, use_container_width=True)

        # FERTILITY RATE CHART
        fertility_rate_df = plot_df[plot_df["Indicator"] == "Fertility Rate"]
        st.subheader("Fertility Rate")
        latest_year_ft = fertility_rate_df[fertility_rate_df["Value"].notnull()]["year"].max()
        current_fertility = fertility_rate_df[fertility_rate_df["year"] == latest_year_ft]["Value"].values[0]
        st.write(f"Current Fertility Rate ({latest_year}): {current_fertility} TFR")
        fertility_rate_chart = (
            alt.Chart(fertility_rate_df)
            .mark_line(point=False, color="#ccffcc")
            .encode(
                x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Value:Q", title="Fertility Rate"),
                tooltip=["year", "Value"]
            )
            .properties(width=800, height=400)
            .interactive()
        )
        st.altair_chart(fertility_rate_chart, use_container_width=True)


