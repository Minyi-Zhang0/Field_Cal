import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def get_column_index(columns,key):
    if key in columns:
        return columns.get_loc(key)
    else:
        return None

if "upload_key" not in st.session_state:
    st.session_state.upload_key = 0
if 'csr_df' not in st.session_state:
    st.session_state.csr_df = pd.read_csv(resource_path('./data/F(CSR)_parameters.csv'))
if 'csr_ab_dependency' not in st.session_state:
    st.session_state.csr_ab_dependency = ['','']

st.title('Field Calculation')
uploaded_files = st.file_uploader("Upload one csv or multiple csv files:",
                                  accept_multiple_files=True,
                                  type="csv",
                                  key=f"upload_{st.session_state.upload_key}")
# st.write(uploaded_files)
st.write(f'Number of csv datasets uploaded: {len(uploaded_files)}')
if len(uploaded_files) > 0:
    if st.button('Clear uploaded files'):
        st.session_state.upload_key += 1
        st.rerun()
    
    with st.container():
        cols_ec = st.columns(2)
        with cols_ec[0]:
            ion_elm = st.text_input('Ion element, e.g. $Ni$',value='Ni')
        with cols_ec[1]:
            ion_low_char = st.text_input('The lower ion charge',value='1')
        st.session_state.csr_ab_dependency[0] = ion_elm
        st.session_state.csr_ab_dependency[1] = ion_low_char
        st.write(f'The ion to be calculated is $\,{ion_elm}^{{{int(ion_low_char)}+}}\,$ and $\,{ion_elm}^{{{int(ion_low_char)+1}+}}\,$')

    if len(uploaded_files) > 1:
        checkbox_same_setting = st.checkbox('Use the same column setting for all files',value=True)

    file_idx = 0
    df_list = []
    column_H_list = []
    column_H2_list = []
    column_Ni_list = []
    column_Ni2_list = []
    for uploaded_file in uploaded_files:
        df_list.append(pd.read_csv(uploaded_file, skiprows=1))
        if len(uploaded_files) > 1 and checkbox_same_setting == True and file_idx >= 1:
            column_H_list.append(column_H_list[0])
            column_H2_list.append(column_H2_list[0])
            column_Ni_list.append(column_Ni_list[0])
            column_Ni2_list.append(column_Ni2_list[0])
            file_idx += 1
            continue
        else: # set selectbox for every file
            # get default location
            H_loc = get_column_index(df_list[file_idx].columns,'H ion%')
            H2_loc = get_column_index(df_list[file_idx].columns,'H2 ion%')
            # Ni_loc = get_column_index(df_list[file_idx].columns,'Ni ion%')
            # Ni2_loc = get_column_index(df_list[file_idx].columns,'Ni2 ion%')
            Ni_loc = None
            Ni2_loc = None
            with st.container(border=True):
                st.write(f'Select columns for file {file_idx}. \n file name: {uploaded_files[file_idx].name}')
                column_H_list.append(st.selectbox("Select $\,H^+\,$ column",df_list[file_idx].columns, index=H_loc,key=f'selectbox_H_{file_idx}'))
                column_H2_list.append(st.selectbox("Select  $\,2Da\,$  column ($H_2^+$, $D^+$)", df_list[file_idx].columns, index=H2_loc,key=f'selectbox_H2_{file_idx}'))
                column_Ni_list.append(st.selectbox(f"Select $\,{ion_elm}^{{{int(ion_low_char)}+}}\,$ column",df_list[file_idx].columns,index=Ni_loc,key=f'selectbox_Ni_{file_idx}'))
                column_Ni2_list.append(st.selectbox(f"Select $\,{ion_elm}^{{{int(ion_low_char)+1}+}}\,$ column",df_list[file_idx].columns,index=Ni2_loc,key=f'selectbox_Ni2_{file_idx}'))
            file_idx += 1
    with st.container(border=True):
        st.write('Input a and b factors from the CSR table')
        st.write('* L Tegg, et al. Microscopy and Microanalysis 30.3 (2024): 466-475.')
        a = st.number_input('a',format='%0.4f')
        b = st.number_input('b',format='%0.4f')
        with st.expander('CSR table'):
            st.dataframe(st.session_state.csr_df)
            st.write('* the CSR data is credited to Navi')
    if st.button('Calculate'):
        H_ratio_list = []
        Ni_ratio_list = []
        fig,ax = plt.subplots(figsize=(8, 6), dpi=100)
        fontsize=20
        ticksize=15
        for ii in range(len(df_list)):
            H_ratio_list.append(df_list[ii][column_H2_list[ii]] / df_list[ii][column_H_list[ii]])
            Ni_ratio_list.append(np.log10(df_list[ii][column_Ni_list[ii]] / (df_list[ii][column_Ni_list[ii]] + df_list[ii][column_Ni2_list[ii]])))
            ax.scatter(H_ratio_list[ii],Ni_ratio_list[ii],alpha=0.3, edgecolors='none')
        ion_low_tex = f'{ion_elm}^{{{int(ion_low_char)}+}}'
        ion_high_tex = f'{ion_elm}^{{{int(ion_low_char)+1}+}}'
        ax.set_xlabel(r'$\frac{2 \, Da}{H}$', fontsize=fontsize)
        ax.set_ylabel(r'$log_{10} \left( \frac{'+ion_low_tex+'}{'+ion_low_tex+'+'+ion_high_tex+ r'} \right)$', fontsize=fontsize)
        ax.tick_params(axis='both', labelsize=ticksize)
        y_ticks = ax.get_yticks()
        csr = 10 ** (-y_ticks) - 1
        F = a * (1 - b/(csr**0.3 + b + 0.256))
        for iy in range(len(y_ticks)):
            ax.axhline(y=y_ticks[iy], linestyle='--', color='gray', linewidth=0.8,zorder=0)
            ax.text(x=ax.get_xlim()[1],y=y_ticks[iy],s=f' {F[iy]:.2f} V/nm', va='center',ha='left',fontsize=ticksize)
        st.pyplot(fig)
        st.write('___________________')
        fig2,ax2 = plt.subplots(figsize=(8, 6), dpi=100)
        # k = np.linspace(y_ticks[0],y_ticks[-1],num=50)
        k = np.linspace(-4,0,num=50)
        csr_k = 10 ** (-k) - 1
        csr_k_r = 1/(10 ** (-k) - 1)
        F_k = a * (1 - b/(csr_k**0.3 + b + 0.256))
        F_k_r = a * (1 - b/(csr_k_r**0.3 + b + 0.256))
        ax2.plot(F_k,k,label=r'$log_{10} \left( \frac{'+ion_low_tex+'}{'+ion_low_tex+'+'+ion_high_tex+ r'} \right)$')
        ax2.plot(F_k_r,k,label=r'$log_{10} \left( \frac{'+ion_high_tex+'}{'+ion_low_tex+'+'+ion_high_tex+ r'} \right)$')
        ax2.set_xlabel('Electric field (V/nm)', fontsize=fontsize)
        # ax2.set_ylabel(r'$log_{10} \left( \frac{'+ion_low_tex+'}{'+ion_low_tex+'+'+ion_high_tex+ r'} \right)$', fontsize=fontsize)
        ax2.legend(fontsize=fontsize)
        st.pyplot(fig2)

        # output as a table
        res_df_tmp_list = []
        for ii in range(len(df_list)):
            csr = 10**(-Ni_ratio_list[ii])-1
            F = a * (1 - b/(csr**0.3 + b + 0.256))
            res_df_tmp = pd.DataFrame({'2Da/H':H_ratio_list[ii],
                                       'Ion_ratio':Ni_ratio_list[ii],
                                       'F(mV)':F,
                                       'raw_data_id':ii,
                                       })
            res_df_tmp_list.append(res_df_tmp)
        res_df = pd.concat(res_df_tmp_list,ignore_index=True)
        res2_df = pd.DataFrame({
                    'k':k,
                    'F_k(V/nm)': csr_k,
                    'F_k_r(V/nm)': csr_k_r,
                })
        with st.expander('Result DataFrame'):
            st.write(res_df)
            st.write(res2_df)

        
        



    
        


    
