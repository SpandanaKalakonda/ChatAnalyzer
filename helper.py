import matplotlib.pyplot as plt
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()
def fetch_stats(sel_user, df):

    words = []
    if sel_user != "Overall":
        df = df[df['user'] == sel_user]
    # Total number of messages
    n = df.shape[0]
    # Total number of words
    for message in df['message']:
        words.extend(message.split())

    # total media
    media = sum(df['message'].str.strip().str.endswith('omitted'))
    # Number of Images
    images = sum(df['message'].str.strip().str.endswith('image omitted'))
    # Number of stickers
    stickers = sum(df['message'].str.strip().str.endswith('sticker omitted'))
    # Number of GIFs
    gifs = sum(df['message'].str.strip().str.endswith('GIF omitted'))
    # Number of Audio files
    audios = sum(df['message'].str.strip().str.endswith('audio omitted'))
    # Number of video files
    videos = sum(df['message'].str.strip().str.endswith('video omitted'))
    # Number of Documents
    docs = sum(df['message'].str.strip().str.endswith('document omitted'))
    # media = images + stickers + gifs + audios + videos + docs

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return n, len(words), media, images, stickers, gifs, audios, videos, docs, len(links)

def most_active_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts().head() / df.shape[0])*100,2).reset_index().rename({'index':'user','user':'percentage'})
    return x, df

def create_wordcloud(sel_user, df):
    f = open('stopwords_tinglish.txt', 'r')
    stop_words = f.read()

    if sel_user != "Overall":
        df = df[df['user'] == sel_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp.astype(str).apply(lambda x: x.str.contains("omitted")).any(axis=1)]

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width = 500, height =500, min_font_size = 10, background_color = 'white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep = " "))
    return df_wc

def monthly_timeline(sel_user, df):
    if sel_user != "Overall":
        df = df[df['user'] == sel_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline


def daily_timeline(sel_user, df):
    if sel_user != "Overall":
        df = df[df['user'] == sel_user]
    d_timeline = df.groupby('date_').count()['message'].reset_index()
    return d_timeline

def week_activity_map(sel_user,df):
    if sel_user != 'Overall':
        df = df[df['user'] == sel_user]
    return df['weekday'].value_counts()

def month_activity_map(sel_user,df):
    if sel_user != 'Overall':
        df = df[df['user'] == sel_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='weekday', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap
def most_common_words(sel_user, df):

    f = open('stopwords_tinglish.txt', 'r')
    stop_words = f.read()

    if sel_user != "Overall":
        df = df[df['user'] == sel_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp.astype(str).apply(lambda x: x.str.contains("omitted")).any(axis=1)]

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_analysis(sel_user, df):
    if sel_user != "Overall":
        df = df[df['user'] == sel_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


    timeline = df.groupby(['year', 'month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] +"-"+str(timeline['year'][i]))
    timeline[time] = time

    plt.plot(timeline[time],timeline['message'])
    plt.xticks(rotation = "vertical")