import hydralit_components as hc
import info,global_settings
from ui import setUI
import streamlit as st
import lib as lib
import templateLoader as tp
import pandas as pd
import json
from streamlit_login_page import streamlit_login_page

from PIL import Image


st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

setUI()
if st.session_state.get('login') is None:
    value = streamlit_login_page(leftText='Partners Sizing Tool',leftSubText='Helps you size opportunities with selected Partners')
    if value is not None and value!='' and value=='sizeme':
        st.session_state['login']=value
        st.experimental_rerun()
else:
    menu_data = [
        {'id':'info','icon':"fas fa-sliders-h",'label':"Sizing Input"},
        {'id':'logout','icon':"fas fa-sign-out-alt",'label':"LogOut"},
    ]

    over_theme = {'txc_active':'#5d5d5d','txc_inactive': '#adadad', 'menu_background':'#f0f2f6'}

    # image = Image.open('sizing.png')

    # col1,col2,col3=st.columns([1,3,15])
    # col1.image(image,width=50)
    # global_settings.getPartnerSelection(col2)


    page = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        hide_streamlit_markers=False, 
        sticky_nav=True, 
        sticky_mode='pinned', 
    )
    change=False
    if st.session_state.get('changepage')!=page or st.session_state.get('loader')==True :
        st.session_state['loader']=False
        change=True
    st.session_state['changepage']=page
    emp=st.empty()
    if change==True:
        emp.markdown('<p class="big-font">...</p>', unsafe_allow_html=True)
        st.session_state['reset']=True
        if st.session_state.get('sizing') is not None:
            del st.session_state['sizing']
        if st.session_state.get('calcul') is not None:    
            del st.session_state['calcul']
        if st.session_state.get('saved') is not None:    
            del st.session_state['saved']

    if page == 'logout':
        del st.session_state['login']   
        st.experimental_rerun()
    if page == 'info':
        info.getPage()    
        
    emp.empty()
    # st.info('''This app has been created by PBS Partner SEs.  
    # For questions or clarifications, open a TMR for a PSE in Powered-by-Snowflake.
    # ''')

