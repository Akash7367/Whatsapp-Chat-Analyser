from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import re 


url = URLExtract()
def fetch_stats(selected_user, df):
    if selected_user != "overall":
        df = df[df['users'] == selected_user]
    
    # Number of messages
    num_messages = df.shape[0]
    
    # Number of words
    words = []
    for msg in df['message']:
        words.extend(msg.split())
    num_words = len(words)
    
    # Number of media messages
    num_media = df[df['message'] == "<Media omitted>\n"].shape[0]
    
    # Number of links shared
    links = []
    for msg in df['message']:
        links.extend(url.find_urls(msg))
    num_links = len(links)
    
    return num_messages, num_words, num_media, num_links

    
#-----------------we can write a simple code for all above code
    # fetch number of media messages
    num_media=df[df["message"]=="<Media omitted>\n"].shape[0]
    
    # fetch no of links shared
    links=[]
    for i in df['message']:
        links.extend(url.find_urls(i))
    num_links = len(links)
    

    #no of messages
    if(selected_user!='overall'):
        df = df[df['users']==selected_user]
    num_message = df.shape[0]
    
    #no of words
    words=[]
    for i in df['message']:
        words.extend(i.split())
    num_words=len(words)
    
    return num_message,num_words,num_media,num_links

def most_busy_user(df):
    x=df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x,df

#------------------WordCloud----------#
def create_wordcloud(selected_user,df):
    if selected_user!='overall':
        df = df[df['users']==selected_user]
    
    #create shape of wordcloud box
    wc  = WordCloud(width=500,height=300,min_font_size=10,background_color='white')
    # df_wc = wc.generate(df['message'].str.cat(sep=" "))
    df_wc = wc.generate(df['message'].astype(str).str.cat(sep=" "))

    return df_wc

#-------Common words----------#
def most_common_words(selected_user,df):
    if selected_user!='overall':
        df = df[df['users']==selected_user]
    
    temp = df[df['users']!="Group_notification"]
    temp = temp[temp['message']!="<Media omitted>\n"]
    
    word=[]
    for i in temp['message']:
        word.extend((i.split()))
    most_common_word=pd.DataFrame(Counter(word).most_common(20))
    
    return most_common_word

#---------analysis for emijis----#
def emoji(selected_user,df):
    if selected_user!='overall':
        df = df[df['users']==selected_user]
    
    #-Define a regex pattern for emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "]+", flags=re.UNICODE
    )
    emojis = []
    for i in df['message']:
        # emojis.extend([c for c in i if c in emoji.EMOJI_DATA])
        emojis.extend(emoji_pattern.findall(i))
        
    emojis_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emojis_df
    
#-------monthly timeline
def monthly_message(selected_user,df):
    if selected_user!='overall':
        df = df[df['users']==selected_user]
    
    timeline=df.groupby(['Year','month_num','month']).count()['message'].reset_index()
    month_year = []
    for i in range(df.shape[0]):
        if i< len(timeline):
            month_year.append((timeline['month'][i] + "-" + str(timeline["Year"][i])))
    month_year
    timeline['time'] = month_year
    return timeline
    
#-----daily timeline
def day_by_day_msg(selected_user,df):
    if selected_user!='overall':
        df = df[df['users']==selected_user]
        
    # df['only_date']=df['Date'].dt.date
    day_msg=df.groupby('only_date').count()['message'].reset_index()
    return day_msg

#------- each day name timeline-----------#
def msg_day_name(selected_user,df):
    if selected_user!='overall':
        df = df[df['users']==selected_user]
    day_name=df.groupby('day_name').count()['message']
    return day_name

#-------- most busiest time---------#
def msg_time(selected_user,df):
    if selected_user!='overall':
        df=df[df['users']==selected_user]
        
    time_msg=df.pivot_table(index='day_name',columns='time_period',values='message',aggfunc='size').fillna(0)
    
    return time_msg
        
        
        
        
    