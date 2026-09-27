import streamlit as st

pages = {
    'Tools':[
        st.Page('page_field_calc.py',title='Field Calculation'),
    ]
}

pg = st.navigation(pages)

with st.sidebar:
    st.title('**Field Calculation**')
    st.write(' ')
    st.write('v1.0')
    st.write('__________________')
    
pg.run()