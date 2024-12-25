import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from Food.visualize import print_wordcloud, print_count_topic, print_bokeh_graph, print_top_10_word, print_top_word
from LDA_model.model import LDAModel


def run(): 
  st.markdown("---")
  #df = pd.read_csv('/content/drive/MyDrive/Food/cc.csv')
  df = pd.read_csv('/content/drive/MyDrive/Food/cc.csv')
  df.rename(columns = {'REVIEW_RAW':'cmt'}, inplace = True)
  df.columns = map(str.lower, df.columns)
  plt.style.use('seaborn-v0_8-colorblind')

  #count_review
  st.subheader('Top 5 Store with Highest #Reviews', divider='rainbow')
  count = df.groupby('store_name')['cmt'].count().sort_values(ascending=False)
  count = count.reset_index().loc[:5]
  count.sort_values('cmt',inplace=True)
  category = count['store_name']
  store_name = count['cmt']
  fig,ax = plt.subplots()
  ax.barh(category,store_name,color='red',edgecolor='black')
  #plt.xticks(fontsize=25, rotation=45)
  #plt.yticks(fontsize=25)
  ax.set_xlabel('#Review')
  ax.set_ylabel('Store_Name')
  plt.title('#Review Times by Store_name')
  st.pyplot(fig)

  st.subheader('Numbers Review By Category', divider='rainbow')
  count = df.groupby('category')['store_name'].count()
  count = count.reset_index()
  count.sort_values('store_name',inplace=True,ascending=False)
  category = count['category']
  store_name = count['store_name']
  fig,ax = plt.subplots()
  ax.bar(category,store_name,color='red',edgecolor='black')
  #plt.xticks(fontsize=25, rotation=45) 
  #plt.yticks(fontsize=25, rotation=45)
  ax.set_xlabel('Category')
  ax.set_ylabel('#Review')
  plt.title('#Store Name by Category')
  st.pyplot(fig)

  st.subheader('Review Length Distribution', divider='rainbow')
  df['text_length'] = df['cmt'].apply(len)
  fig, ax = plt.subplots()
  ax.hist(df['text_length'], bins=20, edgecolor='black',color='red')
  ax.set_xlabel('Text Length')
  ax.set_ylabel('Frequency')
  ax.set_title('Distribution of Text Lengths')
  st.pyplot(fig)

  st.subheader('World Cloud Reviews', divider='rainbow')
  text_combined = ' '.join(df['cmt'])
  # Create a WordCloud object
  from wordcloud import WordCloud
  wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_combined)
  fig, ax = plt.subplots()
  ax.imshow(wordcloud, interpolation='bilinear')
  ax.axis('off')
  st.pyplot(fig)
  st.markdown('---')

def LDA(selected_option):
  df = pd.read_csv('/content/drive/MyDrive/Food/cc.csv')
  df.rename(columns = {'REVIEW_RAW':'cmt'}, inplace = True)
  df.rename(columns = {'STORE_NAME':'store_name'}, inplace = True)
  df.rename(columns = {'CATEGORY':'category'}, inplace = True)
  lda = LDAModel(df, selected_option)
  lda.get_graph()
