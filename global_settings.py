import streamlit as st
import lib as lib
import templateLoader as tp
import pandas as pd
import json

def rerun():
    if st.session_state.get("calcul")==True:
        del st.session_state['sizing']
        del st.session_state['calcul']
        del st.session_state['saved']
        st.session_state['reset']=True
        st.experimental_rerun()

def getPartnerSelection(container):
    det=container.checkbox("Advanced Sizing",value=False)
    if (det==True):
        st.session_state['partner']="H Details"
        return "H Details"
    st.session_state['partner']="H"    
    return "H"     
    # return container.selectbox("Partner:", tp.getTemplateNames(),key='partner',label_visibility='visible',on_change=rerun)

def getSavedScenarioByPartner(advFilter,container): 
    emptyText='Select Saved Scenario...'
    data=tp.getTemplateByName(st.session_state.get("partner"))
    scenarios=pd.DataFrame( lib.getSavedScenarioByPartner(advFilter))
    if len(scenarios)>0:
        sv=scenarios['ID'].tolist()
        sv.insert(0,emptyText)
        savedScen=container.selectbox("Saved:", sv,key='saved',index=0,label_visibility='collapsed')
        if savedScen!=emptyText:
            data=json.loads(scenarios.loc[scenarios['ID'] == savedScen]['INPUTS'].iloc[0]) 
            return data
    return None