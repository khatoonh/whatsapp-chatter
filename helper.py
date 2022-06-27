from wordcloud import WordCloud
from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji as em
extract = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    num_messages = df.shape[0]
    words = []
    for msg in df['messages']:
        words.extend(msg.split())
    num_media=df[df['messages'] =='<Media omitted>\n'].shape[0]
    extractor = URLExtract()
    links = []
    for msg in df['messages']:
        links.extend(extractor.find_urls(msg))
    return num_messages, len(words), num_media,len(links)
def timeline_show(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    monthly_timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time = []
    for i in range(monthly_timeline.shape[0]):
        time.append(monthly_timeline['month'][i] + "-" + str(monthly_timeline['year'][i]))
    monthly_timeline['time'] = time
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return monthly_timeline,daily_timeline
def activity_map(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts(),df['month'].value_counts()
def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    df_pivot=df.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0)
    return df_pivot
def most_busy_user(df):
    x = df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df
def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    f = open('Hinglish_stopwords.txt', 'r')
    stopwords = f.read()
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)
    wc =WordCloud(width=500,height=500,min_font_size=18,background_color='white')
    temp['messages']=temp['messages'].apply(remove_stop_words)
    df_wc=wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc
def  most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    f = open('Hinglish_stopwords.txt', 'r')
    stopwords = f.read()
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    words = []
    for msg in temp['messages']:
        for word in msg.lower().split():
            if word not in stopwords:
                words.append(word)
    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_analysis(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    emojis = []
    for msg in df['messages']:
        emojis.extend([c for c in msg if c in em.UNICODE_EMOJI['en']])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df



