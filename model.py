#%%
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.manifold import TSNE
from utils.preprocessing_word_utils import tokenization
from utils.visualize_utils import  print_count_topic, print_bokeh_graph, print_top_10_word, print_top_word #,print_wordcloud
#%%
class LDAModel:
    def __init__(self, df: pd.DataFrame, n_components: int):
        self.df = df
        self.n_components = n_components

    def preprocessing_df(self, review_col = 'cmt_2'):
        df = self.df.drop_duplicates(subset='cmt', keep="last")
        df.dropna(axis = 0, inplace = True)
        df[review_col] = df.cmt.apply(lambda x: x.replace('\n','. '))
        df[review_col] = df.apply(lambda x: x[review_col].replace(x['store_name'], '') if x['store_name'] in x['cmt_2'] else x['cmt_2'], axis=1)
        return df

    def create_lda_df(self, review_col = 'cmt_2', n_top_words = 20):
        df = self.preprocessing_df()
        data = self.preprocessing_df().loc[:, review_col].tolist()
        LDA = LatentDirichletAllocation(n_components= self.n_components)
        tf_lda = CountVectorizer(
            max_df=0.99,
            max_features=500,
            min_df=0.01,
            tokenizer=tokenization,
            ngram_range=(1,1))

        tf_matrix_lda = tf_lda.fit_transform(data)
        print ("In total, there are {} reviews and {} terms.".format(
            str(tf_matrix_lda.shape[0]), str(tf_matrix_lda.shape[1])
        ))

        lda_feature_name = tf_lda.get_feature_names_out()
        lda_output = LDA.fit_transform(tf_matrix_lda)
        print('Train completed.')
        topic_word = LDA.components_

        n_top_words = n_top_words
        topic_summaries = []

        # topic_word = LDA.components_  # get the topic words
        vocab = tf_lda.get_feature_names_out()

        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
            topic_summaries.append(' '.join(topic_words))
            print('Topic {}: {}'.format(i, ' | '.join(topic_words)))

        tsne_model = TSNE(n_components=4, verbose=1, random_state=42, n_iter=500)
        tsne_lda = tsne_model.fit_transform(lda_output)

        unnormalized = np.matrix(lda_output)
        doc_topic = unnormalized/unnormalized.sum(axis=1)

        lda_keys = []
        for i, tweet in enumerate(df['cmt_2']):
            lda_keys += [doc_topic[i].argmax()]

        lda_df = pd.DataFrame(tsne_lda, columns=['x','y'])
        lda_df['review'] = df['cmt_2']
        lda_df['category'] = df['category']
        lda_df['topic'] = lda_keys
        lda_df['topic'] = lda_df['topic'].map(int)
        return lda_df, topic_word, topic_summaries, vocab

    def get_graph(self):
        df = self.preprocessing_df()
        lda_df, topic_word, topic_summaries, vocab = self.create_lda_df()
        print('print_count_topic')
        print_count_topic(lda_df)
        print('print_bokeh_graph')
        print_bokeh_graph(lda_df, self.n_components, review_col = 'cmt_2', n_top_words = 20, plot_name = 'LDA_plot')
        print('print_top_10_word')
        print_top_10_word(df.cmt_2)
        print('print_top_word')
        print_top_word(topic_word,topic_summaries,vocab, n_word = 10)
        return 'Done'

