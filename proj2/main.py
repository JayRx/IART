import csv

import nltk
import pandas as pd
from nltk.tokenize import *


# nltk.download('punkt')


def main():
    with open("/data/public_dev.csv", newline='') as line:
        reader = csv.reader(line)
        data = list(reader)
    public_text = pd.read_csv("/data/public_dev.csv", header=None)

    # print(data)
    aux = public_text.iloc[1:, 1:2]

    tokens_list = []

    for phrase in data:
        # print( phrase[1])
        tokens = word_tokenize(phrase[1])
        tokens_list.append(tokens)

    # every single list inside tokens_list have the tokens of one possible joke
    tokens_list = tokens_list[1:]

    # print(tokens_list)
    """
    humor_data = pd.read_csv('files/dev.csv')
    
    print("\n----- Head -----")
    print(humor_data.head())
    
    print("\n----- Describe ------")
    print(humor_data.describe())
    """
