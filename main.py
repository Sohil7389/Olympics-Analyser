import matplotlib.pyplot as plt
import streamlit as st
import preprocessor
import helper
import pandas as pd
import plotly.express as px
import seaborn as sns

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis'))

# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + 'Overall Performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Performance in ' + str(selected_year) + ' Olympics')
    st.dataframe(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)

    with col2:
        st.header('City')
        st.title(cities)

    with col3:
        st.header('Sport')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Event')
        st.title(events)

    with col2:
        st.header('Athletes')
        st.title(athletes)

    with col3:
        st.header('Nation')
        st.title(nations)

    nation_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nation_over_time, x='Edition', y='region')
    st.title('Participating Nations Over The Years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title('Events Over The Years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title('Athletes Over The Years')
    st.plotly_chart(fig)

    st.title('No. of Events over time(Every Sport)')
    fig, ax = plt.subplots(figsize=(28, 28))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)
