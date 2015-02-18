#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json,os,math,sys
from collections import defaultdict


def get_langlist(root):
    langlist=[]
    for filename in os.listdir(root):
        with open(root+'/'+filename) as fp:
            lan=json.load(fp)
            langlist.append(lan)
    return langlist

def get_features(text):
    step=1
    n=len(text)
    grams=[]
    for step in range(1,4):
        g=[]
        i=0
        while i+step-1<n:
            g.append(text[i:i+step])
            i+=1
        grams.append(g)
    return grams

def predict(langlist,text,order):
    grams=get_features(text)
    pre_label=''    
    v=sum(language['n_words'][order-1] for language in langlist)
    predict_list=[]
    for language in langlist:
        total_score=0.0
        for feature in grams[order-1]:
            if feature not in language['freq']:
                total_score+=math.log(1.0/v)
            else:
                total_score+=math.log(language['freq'][feature]/float(language['n_words'][order-1]))
        predict_list.append((total_score,language['name']))
    pre_label=max(item for item in predict_list)
    #print sorted(predict_list,reverse=True)[:5]
    return pre_label[1]


if __name__=='__main__':
    ROOT="languages"
    ORDER=2
    langlist=get_langlist(ROOT)
    with open(sys.argv[1],'r') as fr:
        text=fr.read().strip().decode('UTF-8')
    pre_label=predict(langlist,text,ORDER)  
    print "predicted language type is:", pre_label
