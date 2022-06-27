import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import preprocessor,helper
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    #fetch unique user
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show Analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media,links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(links)
        monthly_timeline, daily_timeline = helper.timeline_show(selected_user, df)
        #Monthly Timeline
        st.title("Monthly Timeline")
        fig,ax=plt.subplots()
        ax.plot(monthly_timeline['time'],monthly_timeline['messages'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #Daily Timeline
        st.title("Daily Timeline")
        fig, ax = plt.subplots()
        #plt.figure(figsize=(18, 10))
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # Activity map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        busy_day, busy_month = helper.activity_map(selected_user, df)
        with col1:
            st.header("Most Busy Day")
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        #Activity map
        st.title("Weekly Activity Map")
        activity_map=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(activity_map)
        st.pyplot(fig)

        #finding the busiest user in the group
        if selected_user == 'Overall':
            st.title("Most Busy User")
            x,new_df=helper.most_busy_user(df)
            fig,ax=plt.subplots()
            col1,col2 =st.columns(2)
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #wordcloud
        st.title("WordCloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        #Most common words
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most common words')
        st.pyplot(fig)
        #emoji analysis
        emoji_df=helper.emoji_analysis(selected_user,df)
        st.title('Emoji Analysis')
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)







