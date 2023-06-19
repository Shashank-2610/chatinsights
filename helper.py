import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
extractor = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    #fetch total number of messages
    num_messages = df.shape[0]

    #fetch total number of words
    words = []
    for message in df['messages']:
        words.extend(message.split())

    #fetch total number of media messages
    num_media_messages = df[df['messages']=='<Media omitted>\n'].shape[0]

    #fetch total number of links shared
    urls = []
    for message in df['messages']:
        urls.extend(extractor.find_urls(message))

    return num_messages, len(words),num_media_messages,len(urls)

def most_busy_users(df):
    x = df['users'].value_counts().head()
    new_df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x,new_df

def create_wordcloud(selected_user,df):
    f = open('hinglish_stopwords.txt', 'r')
    stopwords = f.read()

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    temp = temp[temp['messages'] != '<media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)
    wc = WordCloud(width=500, height=500, min_font_size=12, background_color='white')
    temp['messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))

    return df_wc

def top_words(selected_user,df):
    f = open('hinglish_stopwords.txt', 'r')
    stopwords = f.read()

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    temp = temp[temp['messages'] != '<media omitted>\n']
    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    most_common_words = pd.DataFrame(Counter(words).most_common(20))
    return most_common_words

def count_emojis(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI.keys()])
    most_used_emojis = pd.DataFrame(Counter(emojis).most_common(20))

    return most_used_emojis

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    timeline = df.groupby(['only_date']).count()['messages'].reset_index()

    return timeline

def week_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    return df['day_name'].value_counts()

def month_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    user_heatmap = df.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0)

    return user_heatmap