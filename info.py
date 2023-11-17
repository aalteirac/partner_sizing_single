from datetime import datetime
import templateLoader as tp
import global_settings
import streamlit as st
import json
import lib
import re
import time
from datetime import date
import pandas as pd


def get(key):
    return st.session_state.get(key)

def getPage():
    aename,prospname,dealsize,expdate=st.columns(4)
    global_settings.getPartnerSelection(st)
    advFilter=st.session_state.get("partner")
    data=tp.getTemplateByName(advFilter)

    if st.session_state.get('reset')==True:
        st.session_state['prosptext']=''
        st.session_state['aetext']=''
        st.session_state['reset']=False
    # prospect=prospname.text_input('Prospect Name:',label_visibility='visible',placeholder='Enter Prospect Name...',key='prosptext')
  
    # ae=aename.text_input('AE Name:',label_visibility='visible',placeholder='Enter AE Name...',key='aetext')
    # expdate=expdate.date_input("Expected Closing Date:", date.today(),label_visibility='visible',key='estDate')
    # dealsi=dealsize.number_input("Estimated Deal Size:", value=10000,label_visibility='visible',key='dealSize')

    # dis=not ((prospect!='') and (ae!=''))
    dis=False
    sizebtn=st.empty()
    if st.session_state.get("sizing")!=True:
        if sizebtn.button('START SIZING...',disabled=dis):
            st.session_state['sizing']=True
            sizebtn.empty()

    if st.session_state.get("sizing")==True:
         generateInputUI(data)
         ctn=st.container()
         calcbtn=st.empty()
         if st.session_state.get("calcul")!=True:
            if calcbtn.button('CALCULATE'):
                st.session_state['calcul']=True
                calcbtn.empty()
         if st.session_state.get("calcul")==True: 
            generateCalculationUI(data,ctn) 
            checkWarning(data)
            chartMe(data)
            if st.session_state.get("saved")!=True:
                # save(prospect)
                st.session_state['saved']=True
            resetbtn=st.empty()
            if resetbtn.button('SIZE ANOTHER OPPORTUNITY'):   
               del st.session_state['sizing']
               del st.session_state['calcul']
               del st.session_state['saved']
               st.session_state['reset']=True
               resetbtn.empty()
               st.experimental_rerun()   

def generateInputUI(data):
    with st.expander("Input",expanded=True):
        nbcol=2
        if data.get("input_col") is not None:
            nbcol=data.get("input_col") 
        dcol=st.columns(nbcol)
        index=0

        for key in data:
            if key.lower()=="input":
                for kk in data[key]:
                    col=dcol[index]
                    if kk["type"] is not None:
                        if kk["type"].lower()=='number':
                            getNumberInput(kk,col)
                        if kk["type"].lower()=='select':
                            getSelectInput(kk,col)       
                    if kk.get("visibility")!='hidden':
                        index+=1
                    if index>len(dcol)-1:
                        index=0

def generateCalculationUI(data,ctn):
    with ctn.expander("Results",expanded=True):
        nbcol=2
        if data.get("result_col") is not None:
            nbcol=data.get("result_col") 
        dcol=st.columns(nbcol)
        index=0

        for key in data:
            if key.lower()=="calculations":
                for kk in data[key]:
                    col=dcol[index]
                    if kk.get("calc") is not None:
                        calc=replace_words(kk.get("calc"))
                        setCalculationOutput(kk,kk.get("id"),kk.get("label"),eval(calc),'',col)  
                    if kk.get("visibility")!='hidden':    
                        index+=1
                    if index>len(dcol)-1:
                        index=0

def getNumberInput(kk,col):  
    if kk.get('visibility') is not None and kk.get('visibility').lower()=='hidden':
        st.session_state[kk["id"]]=kk.get("default".lower())
    else:    
        if kk.get('default') is None:
            kk["default"]=0
        min=kk.get("rangemin".lower())
        max=kk.get("rangemax".lower())
        step=kk.get("rangestep".lower()) 
        value=kk.get("default".lower())  
        if isinstance(step, float):
            min=float(min)
            max=float(max)
            value=float(value)
        return col.number_input(key=kk["id"],label=kk.get("label".lower()),min_value=min,max_value=max,step=step,value=value)  

def getSelectInput(kk,col):
    disabled=False
    if kk.get('disabled') is not None and kk.get('disabled')==True:
        disabled=True
    if kk.get('visibility') is not None and kk.get('visibility').lower()=='hidden':
        st.session_state[kk["id"]]=kk.get("default".lower())
    else: 
        index=kk.get("entries").index(kk.get("default"))  
        label=kk.get("label")
        if kk.get('suggest') is not None:
            index=eval(replace_words(kk.get("suggest")))
            label+=f' (Reco {kk.get("entries_label")[ index]})'
            if st.session_state.get(kk["id"]) is None:
                st.session_state[kk["id"]]=kk.get("entries")[index] 

        return col.selectbox(disabled=disabled,key=kk["id"],index=index,label=label,options=kk.get("entries".lower()), format_func=lambda x:kk.get("entries_label".lower())[ kk.get("entries".lower()).index(x) ])    

def setCalculationOutput(raw,key,label,value,unit,col):
    st.session_state[key]=value
    if raw.get('visibility') is None or raw.get('visibility').lower()!='hidden':
        if raw.get('entries') is not None:
            return col.text_input(key=key+"_ui",label=label, value=raw.get('entries_label')[raw.get('entries').index(value)], disabled=True)
        else:    
            valF='{:,.0f}'.format(value)
            format=raw.get('format')
            un=raw.get('unit')
            if format is not None:
                unit=''
                if un is not None:
                    unit=un
                valF=f'{unit}{value:{format}}'
            return col.text_input(key=key+"_ui",label=label, value=valF, disabled=True)

def save(prospect):
    data=tp.getTemplateByName(st.session_state.get("partner"))
    # ip=data["input"]
    # for field in ip:
    #     field['default']=get(field['id'])
    # data['input']=ip
    # now = datetime.now()

    # partName=st.session_state.get("partner")
    # prospectName=st.session_state.get("prosptext")
    # aeName=st.session_state.get("aetext")
    # estDate=st.session_state.get("estDate")
    # dealSize=st.session_state.get("dealSize")
    # lib.save(prospect +'_'+st.session_state.get("partner")+' ('+now.strftime("%m/%d/%Y, %H:%M:%S")+')',partName,prospectName,aeName,dealSize,estDate,data)

def checkWarning(data):
    for key in data:
        if key.lower()=="input":
            for kk in data[key]:
                if kk.get("suggest") is not None:
                    calc=st.session_state[kk.get("id")]
                    suggest= replace_words(kk.get("suggest")) 
                    suggest=eval(suggest)
                    valsuggest=kk.get("entries")[suggest]
                    if valsuggest!=calc:
                        st.warning("Warning: Some recommendations have not been followed: " + kk.get("label") + ' is recommended to be ' + kk.get("entries_label")[suggest]+'.')

def replace_words(expression):
    convert=['float','int','warehousecustom']
    pattern = r'\b(?![0-9]+\b)\w+\b'
    def replace(match):
        word = match.group()
        if word in convert:
            return word
        return f'''get('{word}') '''
    output_expression = re.sub(pattern, replace, expression)
    return output_expression

def warehousecustom(param,arrLimit,arrResult):
    res=0
    for idx,lm in enumerate(arrLimit):
        if param<=lm:
            res=arrResult[idx]
            break
        if idx+1<=len(arrLimit)-1:
            if param>=lm and param<=arrLimit[idx+1]:
                res=arrResult[idx]
                break
        else: 
           res=arrResult[idx]
           break    
    return res

def generatePieDef(data,col):
    categories=data.get("categories")
    values=[]
    for cat in categories:
        values.append({"category":cat.get("label"),"value":eval(replace_words(cat.get("measure")) )})
    cdef={
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "A simple donut chart with embedded data.",
        "data": {
            "values": values
        },

        "encoding": {
            "theta": {"field": "value", "type": "quantitative","stack": True},
            "color": {"field": "category", "type": "nominal"}
        },
        "layer": [{
            "mark": {"type": "arc", "innerRadius": 80}
            
            }]
    }
    with col:
        with st.expander(data.get("title"),expanded=True):
            st.vega_lite_chart(cdef, use_container_width=True)

def chartMe(data):
    nbcol=data.get("chart_col") 
    if nbcol is None:
        nbcol=1
    dcol=st.columns(nbcol)
    index=0
    for key in data:
        if key.lower()=="chart":
          for chart in data[key]:
            if chart.get("type")=='pie':
                col=dcol[index]
                generatePieDef(chart,col)
            index+=1
            if index>len(dcol)-1:
                index=0
    