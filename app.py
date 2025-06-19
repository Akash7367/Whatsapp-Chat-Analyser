import streamlit as st
import whatsapp,helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import seaborn as sns


#creating an app or web
st.sidebar.title("Whatsapp Chat Analyser")

#upload file
uploaded_file = st.sidebar.file_uploader("choose a file")
if(uploaded_file is not None):
    bytes_data= uploaded_file.getvalue()
    #fetch data by decoding
    data = bytes_data.decode("utf-8")
    #access my data frame which i made
    df = whatsapp.preprocess(data)
    # st.dataframe(df)
    st.title("Chat Statics")

    #----create a dropdown button such that we can select any user
    #here list of all users
    user_list = df["users"].unique().tolist()
    #remove group notification,add overall,and sort name
    if 'Group_notification' in user_list:
        user_list.remove('Group_notification')

    # user_list.remove('Group_notification')
    user_list.sort()
    user_list.insert(0,"overall")
    
    selected_user=st.sidebar.selectbox("show Analysis w.r.t ", user_list)
    
    #now create a button of showing analysis and 4 column in streamlit page which has total message, total word,and much more
    if st.sidebar.button("show analysis"):
        #create another python file helper such tha all calculation done there
        num_messages,num_words,num_media,num_links=helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)
        #total messages
        with col1:
            st.header("Total Msg")
            st.title(num_messages)
        
        #total Words    
        with col2:
            st.header("total word")
            st.title(num_words)
            
        with col3:
            st.header("total media")
            st.title(num_media)
        with col4:
            st.header("total links")
            st.title(num_links)
        
        #create another title of busy_user
        if(selected_user=='overall'):#its only for group
            st.title("most busy users")
            
            x,new_df=helper.most_busy_user(df) 
            fig, ax = plt.subplots()
            plt.xticks(rotation=70)
            col1, col2 = st.columns(2,gap='large')
            
            with col1:
                ax.bar(x.index,x.values,color = 'red')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)
                
        
        
        ##-------most common words---
        st.title("Most commenly words")
        most_common_word = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots(figsize=(6,4))
        ax.bar(most_common_word[0],most_common_word[1])
        plt.xticks(rotation=80)
        st.pyplot(fig)

        #----- emogi analysis----#
        st.title("all emogies")
        emojis_df = helper.emoji(selected_user,df)
        
        col1,col2 = st.columns(2,gap='large')
        if(emojis_df.empty):
            st.write("no emoji")
        else:
            with col1:
                st.dataframe(emojis_df)    
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emojis_df[1].head(),labels=emojis_df[0].head(),autopct='%0.1f')
                st.pyplot(fig)
                
        #------ message by months------#
        timeline = helper.monthly_message(selected_user,df)
        timeline['time'] = pd.to_datetime(timeline['time'])
        st.title("monthly messages")
        fig, ax = plt.subplots(figsize=(5,2))
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation=85)
        st.pyplot(fig)
        
        #--------message by day-----#
        st.title("messages Day By Day")
        day_msg = helper.day_by_day_msg(selected_user,df)
        # st.dataframe(day_msg)
        fig, ax = plt.subplots(figsize=(5,2))
        ax.plot(day_msg['only_date'],day_msg['message'],color='green')
        plt.xticks(rotation=85)
        st.pyplot(fig)
        
        #----------message by each day name
        day_name = helper.msg_day_name(selected_user,df)
        st.title("each day message")
        fig, ax = plt.subplots(figsize=(4,2))
        ax.bar(day_name.index,day_name.values,color="blue")
        plt.xticks(rotation=85)
        st.pyplot(fig)
        
        #----kaun sa user kab jyada active rahta hai------------#
        st.title("most busiest time")
        time_mg = helper.msg_time(selected_user,df)
        fig, ax = plt.subplots(figsize=(18,9))
        # plt.figure(figsize=(24,7))
        ax = sns.heatmap(time_mg)
        # ax.heatmap(df.pivot_table(index='day_name',columns='time_period',values='message',aggfunc='size').fillna(0))
        plt.yticks(rotation=0)
        st.pyplot(fig)
    
        #-- word cloud-------#
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)