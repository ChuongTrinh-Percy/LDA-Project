import numpy as np
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt

from collections import Counter
from wordcloud import WordCloud

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import bokeh.plotting as bp
import random
from sklearn.manifold import TSNE
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import show, save
from sklearn.manifold import TSNE
from utils.preprocessing_word_utils import *


colormap = list(["#6d8dca", "#69de53", "#723bca", "#c3e14c", "#c84dc9", "#68af4e", "#6e6cd5",
"#e3be38", "#4e2d7c", "#5fdfa8", "#d34690", "#3f6d31", "#d44427", "#7fcdd8", "#cb4053", "#5e9981",
"#803a62", "#9b9e39", "#c88cca", "#e1c37b", "#34223b", "#bdd8a3", "#6e3326", "#cfbdce", "#d07d3c",
"#52697d", "#194196", "#d27c88", "#36422b", "#b68f79"])


# def generate_wordcloud(tup):
#     wordcloud = WordCloud(background_color='white',
#                           max_words=50, max_font_size=40,
#                           random_state=42
#                          ).generate(str(tup))
#     return wordcloud

# def print_wordcloud(df, category_col = 'category', review_col = 'cmt_2', n_word = 100):
#   df = df.iloc[:400]
#   top4 = df[category_col].value_counts()[:4].index.to_list()
#   cat_desc = dict()
#   for cat in df[category_col].unique():
#       text = " ".join(df.loc[df[category_col]==cat, review_col].values)
#       cat_desc[cat] = tokenization(clean_data(text))
#   top1 = Counter(cat_desc[top4[0]]).most_common(n_word)
#   top2 = Counter(cat_desc[top4[1]]).most_common(n_word)
#   top3 = Counter(cat_desc[top4[2]]).most_common(n_word)
#   top4 = Counter(cat_desc[top4[3]]).most_common(n_word)

#   fig,axes = plt.subplots(2, 2, figsize=(30, 15))

#   ax = axes[0, 0]
#   ax.imshow(generate_wordcloud(top1), interpolation="bilinear")
#   ax.axis('off')
#   ax.set_title("top 1", fontsize=30)

#   ax = axes[0, 1]
#   ax.imshow(generate_wordcloud(top2))
#   ax.axis('off')
#   ax.set_title("top 2", fontsize=30)

#   ax = axes[1, 0]
#   ax.imshow(generate_wordcloud(top3))
#   ax.axis('off')
#   ax.set_title("top 3", fontsize=30)

#   ax = axes[1, 1]
#   ax.imshow(generate_wordcloud(top4))
#   ax.axis('off')
#   ax.set_title("top 4", fontsize=30)
#   plt.savefig("./graph_output/four_subplots.png")


def print_top_10_word(df_col_review):
  values, counts = np.unique([' '.join(tokenization(i)) for i in df_col_review], return_counts=True)
  data = pd.DataFrame({'review_word': values, 'count_value':counts})
  data = data.iloc[:1000].nlargest(10, 'count_value')
  plt.figure(figsize=(10,5))
  ax = sns.barplot(x = data.review_word.sort_values(ascending = False),
              y = data.count_value.sort_values(ascending = False),
              order = data.sort_values('count_value', ascending = False).review_word
              )
  ax.set(xlabel='Topic', ylabel='Number of Reviews')

  # Add a title and axis labels
  # plt.title("Topic: 0")
  plt.xticks(rotation=60)
  plt.xlabel("Word Count")
  plt.ylabel("Weights")
  # plt.grid(True)
  # Show the plot
  plt.savefig("./graph_output/print_top_freq_10_word.png")
  # plt.show()


def print_count_topic(lda_df):
  if len(lda_df.topic.value_counts(sort=True)) > 4:
    top_value = 4
  else: top_value = len(lda_df.topic.value_counts(sort=True))
  print('top_4: ', top_value)
  print('lda_df.topic.value_counts(sort=True): ', lda_df.topic.value_counts(sort=True))
  plt.figure(figsize=(8, 6))
  ax = sns.barplot(x = lda_df.topic.value_counts(sort=True)[:top_value].sort_values(ascending = False).index,
              y = lda_df.topic.value_counts(sort=True)[:top_value].sort_values(ascending = False),
              order = lda_df.topic.value_counts(sort=True)[:top_value].sort_values(ascending = False).index)
  ax.set(xlabel='Topic', ylabel='Number of Reviews')
  plt.savefig("./graph_output/top_4_topic.png")
  # plt.show()


def print_bokeh_graph(lda_df, n_components, review_col, n_top_words = 20, plot_name = 'LDA_plot'):
  

  color_maps = random.sample(colormap, n_components)

  lda_df['color'] = lda_df['topic'].apply(lambda x: dict(enumerate(color_maps)).get(x))

  plot_lda = bp.figure(width=700,
                      height=600,
                      title="LDA topic visualization",
      tools="pan,wheel_zoom,box_zoom,reset,hover",
      x_axis_type=None, y_axis_type=None, min_border=1)

  source = ColumnDataSource(data=dict(x=lda_df['x'], y=lda_df['y'],
                                      color=lda_df['color'],
                                      description=lda_df['review'],
                                      topic=lda_df['topic'],
                                      category=lda_df['category']))

  plot_lda.scatter(source=source, x='x', y='y', color='color')

  hover = plot_lda.select(dict(type=HoverTool))
  hover.tooltips={"review":"@description",
                "topic":"@topic", "category":"@category"}

  # show(plot_lda)
  save(plot_lda, './graph_output/'+plot_name+".html")

def print_top_word(topic_word,topic_summaries,vocab, n_word = 10):
  top_word_dict = dict()
  for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(11):-1]
        topic_summaries.append(' '.join(topic_words))
        top_word_dict[i] = topic_words

  topic_df = pd.DataFrame(top_word_dict)
  for num in range(len(topic_df.columns)):
    if num <= 3:
      vars()['top_group'+ str(topic_df.columns[num]+1)] = Counter(topic_df[topic_df.columns[num]]).most_common(n_word)
  plt.figure(figsize=(8, 6))
  fig,axes = plt.subplots(2, 2, figsize=(30, 15))

  ax = axes[0, 0]
  ax.imshow(generate_wordcloud(vars()['top_group'+ str(topic_df.columns[0]+1)]), interpolation="bilinear")
  ax.axis('off')
  ax.set_title("top 1", fontsize=30)

  ax = axes[0, 1]
  ax.imshow(generate_wordcloud(vars()['top_group'+ str(topic_df.columns[1]+1)]))
  ax.axis('off')
  ax.set_title("top 2", fontsize=30)

  ax = axes[1, 0]
  ax.imshow(generate_wordcloud(vars()['top_group'+ str(topic_df.columns[2]+1)]))
  ax.axis('off')
  ax.set_title("top 3", fontsize=30)

  ax = axes[1, 1]
  ax.imshow(generate_wordcloud(vars()['top_group'+ str(topic_df.columns[3]+1)]))
  ax.axis('off')
  ax.set_title("top 4", fontsize=30)
  plt.savefig("./graph_output/top_4_topic_wordcloud.png")
  
