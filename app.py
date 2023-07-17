import pandas as pd
import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    chat = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(chat)

    #st.dataframe(df)

    # unique users

    unique_users = df['user'].unique().tolist()
    for i in unique_users:
        if 'group_notification' in i:
            unique_users.remove('group_notification')
    unique_users.sort()
    unique_users.insert(0,"Overall")

    selected = st.sidebar.selectbox("Show Analysis of", unique_users)
    if st.sidebar.button("Analyze"):
        n, w, m, i, s, g, a, v, d, li = helper.fetch_stats(selected, df)
        st.title("Top Statistics:")
        c1, c2, c3 = st.columns(3)
        c4, c5, c6 = st.columns(3)
        c7, c8, c9, c10 = st.columns(4)

        with c1:
            st.header("Total Messages")
            st.title(n)
        with c2:
            st.header("Total Words")
            st.title(w)
        with c3:
            st.header("Total Media")
            st.title(m)
        with c4:
            st.header("Images")
            st.title(i)
        with c5:
            st.header("Stickers")
            st.title(s)
        with c6:
            st.header("GIFs")
            st.title(g)
        with c7:
            st.header("Audio")
            st.title(a)
        with c8:
            st.header("Video")
            st.title(v)
        with c9:
            st.header("Docs")
            st.title(d)
        with c10:
            st.header("Links")
            st.title(li)
        # Monthly timeline
        st.title("Monthly timeline")
        timeline = helper.monthly_timeline(selected, df)
        fig, ax = plt.subplots()
        plt.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # Daily timeline
        st.title("Daily timeline")
        d_timeline = helper.daily_timeline(selected, df)
        fig, ax = plt.subplots()
        plt.plot(d_timeline['date_'], d_timeline['message'], color='indigo')
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # Activity map
        st.title('Activity Map')
        c1, c2 = st.columns(2)
        with c1:
            st.header("Most Active day")
            active_day = helper.week_activity_map(selected, df)
            fig, ax = plt.subplots()
            ax.bar(active_day.index, active_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with c2:
            st.header("Most Active month")
            active_month = helper.month_activity_map(selected, df)
            fig, ax = plt.subplots()
            ax.bar(active_month.index, active_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # the busiest users in group
        if selected == 'Overall':
            st.title("Most Active Users")
            x, p_df = helper.most_active_users(df)
            fig, ax = plt.subplots()

            c1, c2 = st.columns(2)
            with c1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with c2:
                #st.header("Percentage of Messages")
                st.dataframe(p_df)

        # word cloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # top words used
        most_common_df = helper.most_common_words(selected,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation="vertical")
        st.title("Most Common Words")
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_analysis(selected, df)
        st.title("Emoji Analysis")
        c1, c2 = st.columns(2)
        with c1:
            st.dataframe(emoji_df)
        with c2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels = emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)





