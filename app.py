import pandas as pd
import numpy as np
import datetime as dt
import streamlit as st
import plotly.express as px
import pyspark.sql.functions as F

from PIL import Image
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import IntegerType, StringType, DateType
from plotly.graph_objects import Figure

from session import spark_session, updata
from texts import *


spark: SparkSession = spark_session()
data: DataFrame = updata(spark)


@st.cache_data
def beds_data(start_date: dt.date, end_date: dt.date) -> np.ndarray:
    return np.array(
        data.select(
            F.from_unixtime(
                F.unix_timestamp("date", "yyyy/MM/dd")
            ).alias("date")
            .cast(DateType()),
            \
            F.col("deaths_covid")
            .cast(IntegerType()),
            \
            F.col("inpatient_beds_used_covid")
            .alias("common_beds")
            .cast(IntegerType()),
            # \
            # (F.col("total_staffed_pediatric_icu_beds") +
             # F.col("total_staffed_adult_icu_beds"))
            (F.col("staffed_pediatric_icu_bed_occupancy") +
             F.col("staffed_icu_adult_patients_confirmed_covid"))
            .cast(IntegerType())
            .alias("icu_beds"),
            \
            F.col("state")
            .cast(StringType())
        )
        .dropna()
        .filter((F.col("date") > start_date)
                 & (F.col("date") < end_date))
        .groupBy("state")
        .sum()
        .withColumnRenamed("sum(common_beds)", "common_beds")
        .withColumnRenamed("sum(icu_beds)", "icu_beds")
        .withColumnRenamed("sum(deaths_covid)", "deaths")
        .collect()
    )


def history_data() -> DataFrame:
    return (data.select(
            F.from_unixtime(
                F.unix_timestamp("date", "yyyy/MM/dd")
            ).alias("date")
            .cast(DateType()),
            \
            F.col("deaths_covid")
            .cast(IntegerType()),
            \
            F.col("inpatient_beds_used_covid")
            .alias("common_beds")
            .cast(IntegerType()),
            \
            # (F.col("total_staffed_pediatric_icu_beds") +
             # F.col("total_staffed_adult_icu_beds"))
            (F.col("staffed_pediatric_icu_bed_occupancy") +
             F.col("staffed_icu_adult_patients_confirmed_covid"))


            .cast(IntegerType())
            .alias("icu_beds"),
            \
            F.col("state")
            .cast(StringType())
        )
        .dropna()
        .groupBy("state", "date")
        .sum()
        .withColumnRenamed("sum(common_beds)", "common_beds")
        .withColumnRenamed("sum(icu_beds)", "icu_beds")
        .withColumnRenamed("sum(deaths_covid)", "deaths")
        .sort(F.col("date"))
    )


@st.cache_data
def dates_data() -> np.ndarray:
    return np.array(
        data.select(
            F.from_unixtime(
                F.unix_timestamp("date", "yyyy/MM/dd")
            ).alias("date")
            .cast(DateType())
        )
        .dropna()
        .groupBy("date")
        .sum()
        .sort("date")
        .collect()
    ).reshape(1, -1)[0]


@st.cache_data
def deaths_data(start_date: dt.date, end_date: dt.date) -> np.ndarray:
    return np.array(
        data.select(
            F.from_unixtime(
                F.unix_timestamp("date", "yyyy/MM/dd")
            ).alias("date")
            .cast(DateType()),
            \
            F.col("state")
            .cast(StringType()),
            \
            F.col("deaths_covid")
            .cast(IntegerType())
        )
        .dropna()
        # .fillna(0, "deaths_covid")
        .filter((F.col("date") > start_date)
                 & (F.col("date") < end_date))
        .groupBy("state", "date")
        .sum()
        .withColumnRenamed("sum(deaths_covid)", "deaths_covid")
        .sort("date")
        .collect()
    )


# Plots
@st.cache_data
def map_plot(
    locations: np.ndarray,
    values: np.ndarray,
    pallette: str,
    bed_type: str
) -> Figure:

    st.write('Mapa de ocupacion hospitalaria')
    fig = px.choropleth(
        locations=locations,
        color=values,
        locationmode='USA-states',
        color_continuous_scale=pallette,
        scope='usa',
        labels={'locations':'Estado','color': bed_type},
    )

    fig.update_layout(
        geo_scope='usa',
        margin=dict(t=0, b=0, l=0, r=0),
    )

    return fig


@st.cache_data
def deaths_plot(dates: np.ndarray, deaths: np.ndarray) -> Figure:

    fig = Figure()

    st.write('(Barras) Muertes totales. (Linea) Muertes acumuladas')
    fig.add_trace(px.histogram(
        x=dates,
        y=deaths,
        opacity=0.75,
        color_discrete_sequence=['black'],
        title="Muertes totales",
    ).data[0])

    fig.add_trace(px.line(
        x=dates,
        y=deaths.cumsum() / 20,
        color_discrete_sequence=['grey'],
        title="Muertes acumuladas"
    ).data[0]) 
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=True)

    return fig


@st.cache_data
def history_plot(dates, values, toggle: str) -> Figure:

    if toggle == "icu_beds":
        value = "Cama icu"
        color = px.colors.sequential.OrRd[::-1]
    if toggle == "common_beds":
        value = "Cama comun"
        color = px.colors.sequential.PuBu[::-1]
    if toggle == "deaths":
        value = "Muertes"
        color = px.colors.sequential.Greys[::-1]

    fig = px.histogram(
        x=dates,
        y=values,
        nbins=80,
        opacity=0.75,
        color_discrete_sequence=color,
        labels={'y': value, 'x': 'Tiempo'}
    )
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig


@st.cache_data
def top5(df: pd.DataFrame, toggle: str) -> Figure:

    if toggle == "icu_beds":
        value = "Cama icu"
        color = px.colors.sequential.OrRd

    if toggle == "common_beds":
        value = "Cama comun"
        color = px.colors.sequential.PuBu

    if toggle == "deaths":
        value = "Muertes"
        color = px.colors.sequential.Greys

    fig = px.bar(
        df[:5],
        y="Estado",
        x=value,
        text=value,
        color="Estado",
        color_discrete_sequence=color[::-1]
    )
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))

    return fig



def run():

    st.set_page_config(
        page_title="Dashboard PI2",
        layout="wide",
    )

    st.title("Nicolas Palermo")
    st.text(banner)
    st.header(header1)
    st.subheader(subheader1)
    # st.header("Mapa de camas por estado")


    # Control de fechas
    min_date: dt.date = dt.datetime(2020, 4, 12).date()
    max_date: dt.date = dates_data().max()

    start_date, end_date = st.select_slider("Rango de Fecha", options=dates_data()[102:], value=(min_date, max_date))

    if start_date < end_date:
        pass
    else:
        st.error('Error: La fecha limite debe ser posterior a la fecha de inicio.')


    placeholder = st.empty()
    with placeholder.container():


        # Alternar mapas
        beds_state: np.ndarray = beds_data(start_date, end_date)[:, 0].astype(str)
        deaths_beds: np.ndarray = beds_data(start_date, end_date)[:, 1].astype(np.int32)
        common_beds: np.ndarray = beds_data(start_date, end_date)[:, 2].astype(np.int32)
        icu_beds: np.ndarray = beds_data(start_date, end_date)[:, 3].astype(np.int32)

        deaths_date: np.ndarray = deaths_data(start_date, end_date)[:, 1]
        total_deaths: np.ndarray = deaths_data(start_date, end_date)[:, 2]

        select_map = st.radio("Selecciona un tipo de dato", ("Camas comunes", "Camas UCI", "Muertes"))

        mapa, deaths, df = st.columns((10, 12, 3))


        with deaths:
            st.plotly_chart(
                deaths_plot(deaths_date, total_deaths),
                use_container_width=True
            )


        if select_map == "Camas UCI":
            print('debug select UCI')

            history_toggle = "icu_beds"

            with mapa:
                st.plotly_chart(map_plot(
                    beds_state,
                    icu_beds,
                    'OrRd',
                    'UCI',
                ), use_container_width=True)

            with df:

                dframe = (
                    pd.DataFrame({"Estado": beds_state, "Cama icu": icu_beds})
                    .sort_values("Cama icu", ascending=False)
                    .reset_index(drop=True)
                )
                st.write(
                    dframe[:10].style.hide_index().to_html(),
                    width=400,
                    height=1000,
                    use_container_width=True,
                    unsafe_allow_html=True,
                )

        elif select_map == "Camas comunes":
            print('debug select comunes')

            history_toggle = "common_beds"

            with mapa:
                st.plotly_chart(map_plot(
                    beds_state,
                    common_beds,
                    'PuBu',
                    'Comun',
                ), use_container_width=True)

            with df:

                dframe = (
                    pd.DataFrame({"Estado": beds_state, "Cama comun": common_beds})
                    .sort_values("Cama comun", ascending=False)
                    .reset_index(drop=True)
                )
                st.write(
                        dframe[:10].style.hide_index().to_html(),
                    width=400,
                    height=1000,
                    use_container_width=True,
                    unsafe_allow_html=True,
                )

        else:
            history_toggle = "deaths"

            with mapa:
                st.plotly_chart(map_plot(
                    beds_state,
                    deaths_beds,
                    'Greys',
                    'Deaths',
                ), use_container_width=True)

            with df:

                dframe = (
                    pd.DataFrame({"Estado": beds_state, "Muertes": deaths_beds})
                    .sort_values("Muertes", ascending=False)
                    .reset_index(drop=True)
                )
                st.write(
                    dframe[:10].style.hide_index().to_html(),
                    width=400,
                    height=1000,
                    use_container_width=True,
                    unsafe_allow_html=True,
                )


    placeholder2 = st.empty()
    with placeholder2.container():

        option_state = st.selectbox('Selecciona un Estado', sorted(beds_state))
        history, bar = st.columns((14, 10))

        x_history: np.ndarray = (
            np.array(
                history_data().select("date")
                .filter(
                    (F.col("date") > start_date)
                    & (F.col("date") < end_date)
                    & (F.col("state") == option_state)
                )
                .collect()
            ).reshape(1, -1)[0]
        )

        y_history: np.ndarray = (
            np.array(
                history_data().select(history_toggle)
                .filter(
                    (F.col("date") > start_date)
                    & (F.col("date") < end_date)
                    & (F.col("state") == option_state)
                )
                .collect()
            ).reshape(1, -1)[0]
        )

        with history:
            st.write(f'Dato historico de {option_state}')
            st.plotly_chart(history_plot(
                x_history,
                y_history,
                history_toggle
            ), use_container_width=True)


        with bar:
            st.write(f'Top 5')
            st.plotly_chart(top5(
                dframe,
                history_toggle
            ), use_container_width=True)

    # st.subheader(consigna1)
    # st.subheader(consigna2)
    # st.subheader(consigna3)
    # st.subheader(consigna4)
    # st.subheader(consigna5)
    # st.subheader(consigna6)
    # st.subheader(consigna7)
    # st.subheader(consigna8)
    # st.subheader(consigna9)


if __name__ == "__main__":
    run()
