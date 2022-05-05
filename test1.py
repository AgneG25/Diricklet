import os
import streamlit as st
import numpy
os.environ['R_HOME'] = r"C:\Program Files\R\R-4.1.3"
#os.environ['R_USER'] = r"C:\Python39\Lib\site-packages\rpy2"

import subprocess
subprocess.run('conda install -c conda-forge r-base', shell=True)
!pip install rpy2
from rpy2 import robjects

def main():

    catPen = st.number_input('Insert Category Penetration')
    st.write('Category Penetration is ', catPen)

    buyRate = st.number_input('Buyer`s Average Purchase Rate')
    st.write('Purchase Rate is ', buyRate)

    if "brandShare" not in st.session_state:
        st.session_state.brandShare = ['example']

    if "brandPen" not in st.session_state:
        st.session_state.brandPen = ['example']

    if "brandName" not in st.session_state:
        st.session_state.brandName = ['example']

    def insert_elements1(ele1):
        if st.session_state.brandShare:
            st.session_state.brandShare.append(ele1)

    def insert_elements2(ele2):
        if st.session_state.brandPen:
            st.session_state.brandPen.append(ele2)
    
    def insert_elements3(ele3):
        if st.session_state.brandName:
            st.session_state.brandName.append(ele3)


    def fill_form():
        with st.form(key = 'myform', clear_on_submit=True):
            ele1 = st.number_input("Enter brand share: ", key = 'ele1')
            ele2 = st.number_input("Enter brand penatration: ")
            ele3 = st.text_input("Enter brand name: ")
            submit_button = st.form_submit_button("Append")
            calculate_button = st.form_submit_button("Calculate")
            if submit_button:
                insert_elements1(ele1)
                st.write(st.session_state.brandShare)
                insert_elements2(ele2)
                st.write(st.session_state.brandPen)
                insert_elements3(ele3)
                st.write(st.session_state.brandName)
            if calculate_button:
                brandShare=tuple(st.session_state.brandShare)
                brandShare = brandShare[1:]
                brandPen=tuple(st.session_state.brandPen)
                brandPen = brandPen[1:]
                brandName=tuple(st.session_state.brandName)
                brandName = brandName[1:]
                dobj = robjects.r(f'''
                    library(NBDdirichlet)
                    cat.pen <- {catPen} # Category Penetration
                    cat.buyrate <- {buyRate} # Category Buyer's Average Purchase Rate in a given period.
                    brand.share <- c{brandShare} # Brands' Market Share
                    brand.pen.obs <- c{brandPen} # Brand Penetration
                    brand.name <- c{brandName}
                    dobj <- dirichlet(cat.pen, cat.buyrate, brand.share, brand.pen.obs, brand.name)
                    return(dobj)
                ''')
                st.text(dobj)
                st.balloons()

    fill_form()

if __name__ == '__main__':
    main()
