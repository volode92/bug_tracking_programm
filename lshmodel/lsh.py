import numpy as np
import pandas as pd
from datasketch import MinHash, MinHashLSHForest
import string
from initialization import init as initail
import os


class Forest_search():
    def __init__(self):
        self.pathdirect = initail.pathdirect
        self.df = self.upd_df()
        self.tt = str.maketrans(dict.fromkeys(string.punctuation))
        self.permutations = 256
        self.num_recommendations = 10
        self.forest = self.get_forest(self.df, self.permutations)


    def upd_df(self):
        df = pd.DataFrame()
        for subdir, dirs, files in os.walk(self.pathdirect):
            for f in files:
                filename = os.fsdecode(f)
                if filename.endswith(".csv"):
                    if f == 'testlist.csv':
                        continue
                    tmp_df = pd.read_csv(subdir + '/' + f)
                    tmp_df = tmp_df['err_text']
                    df = pd.concat([df, tmp_df], ignore_index=True, sort=False)
        df.columns = ['err']
        return df

   # def preprocess(self, text):
   #     text = str(text)
   #     text = text.translate(self.tt).lower()
   #     text = text.split()
   #     if len(text) < 2:
   #         return [str(" ".join(text))]
   #     tmp = []
   #     for i in range(len(text)-2):
   #         tmp_el = str(" ".join(text[i:i+3]))
   #         tmp.append(tmp_el)
   #     return tmp

    def preprocess(self, text):
        text = str(text)
        text = text.translate(self.tt).lower()
        text = text.split()
        return text

    def get_forest(self, data, perms):

        minhash = []

        for text in data['err']:
            tokens = self.preprocess(text)
            m = MinHash(num_perm=perms)
            for s in tokens:
                m.update(s.encode('utf8'))
            minhash.append(m)

        forest = MinHashLSHForest(num_perm=perms)

        for i, m in enumerate(minhash):
            forest.add(i, m)

        forest.index()

        return forest

    def predict(self, text):

        tokens = self.preprocess(text)
        m = MinHash(num_perm=self.permutations)
        for s in tokens:
            m.update(s.encode('utf8'))

        idx_array = np.array(self.forest.query(m, self.num_recommendations))
        if len(idx_array) == 0:
            return ['таких сочетаний ее нет']  # if your query is empty, return none

        result = list(self.df.iloc[idx_array]['err'])
        result = list(set(result))
        def count_el(x):
            tmp = set(self.preprocess(x))
            tmp2 = set(self.preprocess(text))
            rez = tmp2.intersection(tmp)
            return len(rez)

        result.sort(key=lambda x: count_el(x), reverse=True)
        return result
