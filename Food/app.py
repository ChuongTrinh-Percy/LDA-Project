import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from home import run
from home import LDA

apps = [{"title": "DATASET", "icon": "cast"},
{"title": 'VISUALIZATION', "icon": "braces"},
{"title": "LDA MODEL", "icon": "activity"}]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0


st.sidebar.header("FILTER TAB")

st.title('FOOD REVIEW TOPIC DATASET')
st.header('TABLE OF REVIEW BY STORE NAME', divider='rainbow')

@st.cache_resource
def data_input():
    df_review = pd.read_csv('/content/drive/MyDrive/Food/data_cat.csv')
    df_review.dropna(inplace=True)
    df_review.reset_index(inplace=True,drop=True)
    df_review.sort_values('store_name',ascending=True,inplace=True)
    return df_review.iloc[:10000,:]

df = data_input()
df['DATE'] = pd.to_datetime(df['time_cmt'], format='%d/%m/%Y %H:%M')
df["DATE"] = df['DATE'].dt.strftime('%m/%Y')
df = df.rename(columns={'store_name': 'STORE_NAME',"DATE":"DATE",'time_cmt': 'DATETIME', 'cmt': 'REVIEW_RAW','cmt_2': 'REVIEW_CLEAR','category' : "CATEGORY"})
df = df[['STORE_NAME',"DATE","DATETIME","CATEGORY","REVIEW_RAW"]]

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)
    df = bytes_data

makes = list(df['CATEGORY'].drop_duplicates())
makes = [x for x in makes if str(x) != 'nan']
makes = st.sidebar.multiselect('Select Store Category:', makes)
if len(makes) == 0:
  df = df
else:
  df = df.loc[df["CATEGORY"].isin(makes)]

store = df['STORE_NAME'].unique()
store = st.sidebar.multiselect('Select Store Name:', list(store))
if len(store) == 0:
  df = df
else:
  df = df.loc[df["STORE_NAME"].isin (store)]

start_date = df['DATE'].sort_values(ascending=True).drop_duplicates()
start_date = st.sidebar.selectbox('Select Date From:', start_date)
if len(start_date) == 0:
  df = df
else:
  df = df.loc[(df['DATE'] > start_date)]

df.sort_values(['CATEGORY',"STORE_NAME"],ascending=False,inplace=True)
df.reset_index(inplace=True,drop=True)

st.dataframe(
    df,
    column_config={
        "widgets": st.column_config.Column(
            width="large"
        )
    },height = 300
)

if st.button('EXPLORE REVIEW DATASET',type="primary"):
    df.to_csv('cc.csv')
    print('Import Data_Cat')
    default_index = 1
    run()



selected_option = st.selectbox('How Many Topics Users to Segment', ['1', '2', '3','4','5','6','7','8','9','10'])

if st.button('RUN LDA MODEL',type="primary"):
    df.to_csv('cc.csv')
    print('RUN LDA MODEL')
    LDA(int(selected_option))
    default_index = 2

with st.sidebar:
    selected = option_menu(
        "FUNCTIONS",
        options=titles,
        icons=icons,
        default_index=default_index,
    )

with st.sidebar:
    st.sidebar.title("About us")
    st.sidebar.info(
        """
        Contributed by Ngoc_Anh & Nguyen Chuong  

    """) 
