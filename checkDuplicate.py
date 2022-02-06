# -*- coding: utf-8 -*-
"""
Created on 11/11/2021

@author: Mobisoftech India Pvt. Ltd.
@filename: checkDuplicate.py
@project: AI Based Analysis System
@description: Find the duplicates in the uploaded excel file
"""

# GUI API
import streamlit as st
# Excel API
import pandas as pd
# Image API
from PIL import Image
# Import Datetime
from datetime import datetime


def get_file_name(excel_file):
    """
    get the filename from the uploaded file to utilise it to give name to saved files
    """
    filename = excel_file.name.split(".")[0]

    return filename


def get_excel_df(excel_file):
    """
    get the pandas dataframe from the uploaded excel file for other relevant operations
    """
    df = pd.read_excel(excel_file, engine='openpyxl').dropna()
    return df


def save_the_excel_with_duplicates(excel_file):
    """
    Function to save the excel file after identifying the duplicates by color coding
    """
    df = get_excel_df(excel_file)
    df_arranged = pd.concat(group[1] for group in df.groupby(['Material Number'], sort=False))
    # Returns True for the duplicate rows
    bool_series = df[['Material Number']].duplicated(keep=False)
    # get the indices of the duplicate rows(up to index) and then get the value of it(values)
    duplicate_rows = bool_series[bool_series].index.values
    date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")

    filename = get_file_name(excel_file) + f"_analysed_{date}.xlsx"
    # noinspection PyTypeChecker
    df_arranged.style.apply(lambda x: ['background-color: #d1ca3b' if x.name in duplicate_rows else '' for i in x],
                            axis=1).to_excel(filename)


def save_only_duplicates_as_excel(excel_file):
    """
    Function to extract only the duplicates and save to an excel file
    """
    df = get_excel_df(excel_file)
    df.sort_values("Material Number", inplace=True)
    duplicates = df[df.duplicated(["Material Number"], keep=False)]
    date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")
    filename = get_file_name(excel_file) + f"_duplicates_{date}.xlsx"
    duplicates.to_excel(filename)


def show_excel_with_duplicates(excel_file):
    """
    Function to show the excel in the screen, duplicates are shown by using color coding.

    break the problem into two steps rather than use one complicated lambda function.
    We can find the index of all the duplicate rows, then highlight the rows by index number.
    Also don't forget that in your lambda function, you should use a list comprehension in what
    you are returning.
    """
    df = get_excel_df(excel_file)
    df_arranged = pd.concat(group[1] for group in df.groupby(['Material Number'], sort=False))
    bool_series = df[['Material Number']].duplicated(keep=False)
    duplicate_rows = bool_series[bool_series].index.values
    st.dataframe(df_arranged.style.apply(lambda x: ['background-color: #F09A88' if x.name in duplicate_rows else '' for i in x],
                                         axis=1))


def main_fun():
    """
    main function
    """
    hide_st_style = """
                <style>
                footer:after{
                content: '© 2022 Numaligarh Refinery Limited';
                visibility: visible;
                display:block;
                position:relative;
                color:tomato;
                #background-color: red;
                padding: 5px;
                top: 2px;
                }
                 footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    image = Image.open('nrl-logo.jpg')
    st.image(image)
    st.title("AI Based Analysis System")
    file = st.file_uploader("Choose a File . . .", type=['csv', 'xlsx'])

    analyse = st.button("Analyse")
    save_excel = st.button("Download Analysed File")
    only_duplicates = st.button("Download Only Duplicates")

    if analyse:
        if file is not None:
            show_excel_with_duplicates(file)
            st.success('File successfully analysed !')
        else:
            st.warning("Please upload a file")

    if save_excel:
        if file is not None:
            save_the_excel_with_duplicates(file)
            st.success('Successfully download analysed file!')
        else:
            st.warning("Please upload a file")

    if only_duplicates:
        if file is not None:
            save_only_duplicates_as_excel(file)
            st.success('Successfully download duplicate file!')
        else:
            st.warning("Please upload a file")


if __name__ == "__main__":
    main_fun()
