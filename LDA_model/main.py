from model import LDAModel
import pandas as pd


if __name__ == '__main__':
    df = pd.read_csv('data_cat.csv')
    lda = LDAModel(df, 7)
    lda.get_graph()
