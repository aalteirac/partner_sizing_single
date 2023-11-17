import json
import os
import streamlit as st

dir_path = r'./templates/'


def getTemplateNames():
    names=[]
    res=getTemplates()
    for x in res:
        dt=getTemplate(x)
        names.append(dt['name'])
    return names    

# @st.cache_data(show_spinner=False,ttl=500)
def getTemplateByName(name):
    res=getTemplates()
    for x in res:
        dt=getTemplate(x)
        if (dt['name']==name):
            return dt
  

def getTemplates():
    res = []
    for file_path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, file_path)):
            res.append(dir_path+file_path)
    return res

def getTemplate(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

