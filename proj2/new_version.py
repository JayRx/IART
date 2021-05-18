#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 15 09:58:17 2021

@author: flavio
"""

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer

from nltk.tokenize import PunktSentenceTokenizer # unsupervised machine learning sentence tokenizer , can be trained, but we use the default



def process_content_diff_tokenizers(data_list,tokenizer):
    tk_word_list = []
    
   
    
    
    
    for phrase in data_list:
        text = phrase[0]
        #Tokenization by words or sentences
        tokens = tokenizer.tokenize(text)
        
        tk_word_list.append(tokens)
        
    
    return tk_word_list

def process_content_tagging(text_tokenized):
    res =[]
    for phrase in text_tokenized:
        aux = [] # one list for every tags of one phrase
        for word in phrase:
            
            words = nltk.word_tokenize(word)
            tagged = nltk.pos_tag(words)
            aux.append(tagged)
        res.append(aux)    
    return res        

def chunk_gram_process_content(text_tokenized):
    res = []
    for phrase in text_tokenized:
        aux  = []
        for word in phrase:
            
            words = nltk.word_tokenize(word)
            tagged = nltk.pos_tag(words)
            #any form of adverb
            chunk_gram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
            chunk_parser = nltk.RegexpParser(chunk_gram)
            chunked = chunk_parser.parse(tagged)
            chunked.draw()
            aux.append(chunked)
        res.append(aux)

    return res              
dataset = pd.read_csv('/home/flavio/Desktop/IART2/proj2/files/train.csv')
dataset2 = pd.read_csv('/home/flavio/Desktop/IART2/proj2/files/public_dev.csv')

#print(dataset)
raw_text =""
raw_text2 =""
data_list =[]
data_list2=[]
for i in range(0,8000):
    # get review and remove non alpha chars
   aux_reader = dataset['text'][i]
    
   raw_text += aux_reader+ "\n"
   
   
   data_list.append([aux_reader])
   
for i in range(0,1000):
    # get review and remove non alpha chars
   aux_reader = dataset2['text'][i]
    
   raw_text2 += aux_reader+ "\n"
   
   
   

#Remove stopwords

stop_words = tuple(set(stopwords.words("english")))


#word tokenization, without stopwords
tokens_word_list =[]
for phrase in data_list:
    
    #Tokenization by words or sentences
    tokens = word_tokenize(phrase[0])
    
    tokens_word_list.append(tokens)




#print(stop_words)

filtered_tk_word_list = []

#word tokenization, with stopwords
for phrase in tokens_word_list:
    new_ph = []
    for word in phrase:
        
        if word not in stop_words:
            new_ph.append(word)
        
    filtered_tk_word_list.append(new_ph)

#print( filtered_tk_word_list)



"""
#Stemming, não é particularmente necessário

ps = PorterStemmer()
filt_stem_w_l = []
for phrase_tk in filtered_tk_word_list:
    aux_list = []
    for word in phrase_tk:
        aux = ps. stem(word)
        aux_list.append(aux)
        
    filt_stem_w_l.append(aux_list)

"""

"""
#usar outro tipo de tokenizer p4, arranjar outras piadas para o treinar
p_sent_tk = PunktSentenceTokenizer(raw_text2)

psent_tk_word_list = process_content_diff_tokenizers(data_list,p_sent_tk) #este tokenizer é possível treina-lo

#print(psent_tk_word_list)


"""
#########################################################

#speech-tagging
#res = process_content_tagging(filtered_tk_word_list)

#print( res)

#print(filtered_tk_word_list)

#####################################################
#Chunking (Use Regular expressions)
res2 = chunk_gram_process_content(filtered_tk_word_list)

print (res2)