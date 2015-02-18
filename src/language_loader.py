#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json,os,math
from collections import defaultdict


def get_distributions(root,distribution_list,label_list):
    langlist=[]
    for filename in os.listdir(root):
        if filename in ['en','fr']:
            with open(root+'/'+filename) as fp:
                lan=json.load(fp)
                langlist.append(lan)
    
    for language in langlist:
        distribution=defaultdict(lambda:defaultdict(float))
        for key in language['freq']:
            n=len(key)
            distribution[n-1][key]=float(language['freq'][key])/language['n_words'][n-1]
        label_list.append(language['name'])
        distribution_list.append(distribution)
    return distribution_list,label_list

def get_langlist(root):
    langlist=[]
    for filename in os.listdir(root):
        if filename in ['en','fr']:
            with open(root+'/'+filename) as fp:
                lan=json.load(fp)
                langlist.append(lan)
    return langlist

def get_features(text):
    step=1
    n=len(text)
    grams=dict()
    for step in range(1,4):
        grams[step]=[]
        i=0
        while i+step-1<n:
            grams[step].append(text[i:i+step])
            i+=step
    return grams



def predict(langlist,text):
    features=get_features(text)
    pre_label=''
    pre_score=float('-infinity')
    for language in langlist:
        total_score=0.0
        for dimension in features:
            for feature in features[dimension]:
                if feature not in language['freq']:
                    total_score+=math.log(1.0/language['n_words'][dimension-1])
                else:
                    total_score+=math.log(language['freq'][feature]/float(language['n_words'][dimension-1]))
        if pre_label=='' or total_score>pre_score:
            pre_label=language['name']
            pre_score=total_score
    return pre_label

def classify(distribution_list,label_list,text):
    features=get_features(text)
    pre_label=''
    pre_score=float('-infinity')
    for (i,language) in enumerate(label_list):
        distribution=distribution_list[i]
        total_score=0.0
        for feature in features:
            total_score+=math.log(distribution[0][feature])
        if pre_label=='' or total_score>pre_score:
            pre_label=language
            pre_score=total_score
    return pre_label


if __name__=='__main__':
    root='../languages'
    '''
    distribution_list=[]
    label_list=[]
    get_distributions(root,distribution_list,label_list)
    '''
    langlist=get_langlist(root)
    text="I like swimming"
    with open('test.txt','r') as fr:
        text=fr.read().strip()
    pre_label=predict(langlist,text)  
    print pre_label
