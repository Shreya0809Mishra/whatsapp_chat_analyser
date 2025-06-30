import os

import helper
import preprocessor

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import wordcloud
import helper
import seaborn as sns
from helper import emoji_helper

st.sidebar.title("Whatsapp chat analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    st.dataframe(df)

    #fetch unique user
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages, words,num_media_messages= helper.fetch_stats(selected_user,df)
        col1, col2, col3= st.columns(3)
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total words')
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(num_media_messages)

        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)

        st.title("WEEK ACTIVITY ANALYSIS")
        col1, col2= st.columns(2)
        with col1:
            st.header('MOST BUSY DAY')
            busy_day=helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header('MOST BUSY MONTH')
            busy_month=helper.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        user_heatmap=helper.weekly_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        if selected_user=='Overall':
            st.title('Most busy users')
            x,new_df=helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2= st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.header('Involvement percentage')
                st.dataframe(new_df)
        df.wc=helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df.wc)
        st.pyplot(fig)
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()

        ax.barh(most_common_df['Word'],most_common_df['Count'],color='red')
        plt.xticks(rotation='vertical')
        st.title('MOST COMMON WORDS')
        st.pyplot(fig)

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)

















