import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# Page title
st.set_page_config(page_title='Collection Data ', page_icon='📊')
st.title('📊  Data ')

with st.expander('About this app'):
  st.markdown('**What can this app do?**')
  st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation and editable dataframe for data interaction.')
  st.markdown('**How to use the app?**')
  st.warning('To engage with the app, 1. Select genres of your interest in the drop-down selection box and then 2. Select the year duration from the slider widget. As a result, this should generate an updated editable DataFrame and line plot.')
  
st.subheader('Which Movie Genre performs ($) best at the box office?')

# Load data
df = pd.read_csv('data/StreamliteColl_4.csv')
df.year = df.year.astype('int')
df.month = df.month.astype('int')

# Input widgets
## Genres selection
CBU_list = df.CBU.unique()
CBU_selection = st.multiselect('Select CBU', CBU_list, ['AS', 'JZBU', 'BA', 'NJ'])

## Year selection
year_list = df.year.unique()
year_selection = st.slider('Select year duration',2000,2024, (2022, 2024))
year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))

## month selection
month_list = df.month.unique()
month_selection = st.slider('Select month duration',1,12, (9, 12))
month_selection_list = list(np.arange(month_selection[0], month_selection[1]+1))

df_selection = df[df.CBU.isin(genres_selection) & df['year'].isin(year_selection_list) & df['month'].isin(month_selection_list)]
df_selection['Amount'] = pd.to_numeric(df_selection['Amount'], errors='coerce')
df_selection['year'] = df_selection['year'].astype(int)
df_selection['Amount'] = df_selection['Amount'].astype(float)
reshaped_df = df_selection.pivot_table(index='year', columns='CBU', values='Amount', aggfunc='sum', fill_value=0)
reshaped_df = reshaped_df.sort_values(by='year', ascending=False)


# Display DataFrame

df_editor = st.data_editor(reshaped_df, height=212, use_container_width=True,
                            column_config={"year": st.column_config.TextColumn("Year")},
                            num_rows="dynamic")
df_chart = pd.melt(df_editor.reset_index(), id_vars='year', var_name='CBU', value_name='Amount')

# Display chart
chart = alt.Chart(df_chart).mark_line().encode(
            x=alt.X('year:N', title='Year'),
            y=alt.Y('sum:Q', title='Collection($)'),
            color='CBU:N'
            ).properties(height=320)
st.altair_chart(chart, use_container_width=True)
