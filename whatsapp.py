import re
import pandas as pd
file = open(r"aiml chat.txt",'r',encoding='utf-8')
data=file.read()
# print(data)
def preprocess(data):
    pattern = r"\d{2}/\d{2}/\d{2},\s\d{2}:\d{2}\s-\s"

    messages=re.split(pattern, data)[1:]
    # print(messages)

    dates = re.findall(pattern,data)
    # dates

    # now we have find ,message and dates and now convert it into pandas dataframe to analysisbthe data
    df = pd.DataFrame({"user_message":messages, "message_date":dates})
    df
    # change date into datetime formate
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    df.rename(columns={"message_date":"Date"}, inplace=True)
    # df.head()


    # now create another column of user and message
    user=[]
    messages=[]

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            user.append(entry[1])
            messages.append(entry[2])
        else:
            user.append('Group_notification')
            messages.append(entry[0])
    df['users']=user
    df['message']=messages
    df.drop(columns=["user_message"],inplace=True)
    # df.head(5)

    #now we have splited user and messages and now extract date,month,year from Date
    df['Year'] = df['Date'].dt.year
    df['month']= df['Date'].dt.month_name()
    df['month_num'] = df['Date'].dt.month
    df['Day']=df['Date'].dt.day
    df['day_name']=df['Date'].dt.day_name()
    df['only_date']=df['Date'].dt.date
    df["Hour"]=df['Date'].dt.hour
    df["Minute"]=df['Date'].dt.minute
    period=[]
    df["Hour"]
    for i in df['Hour']:
        if(i==23):
            period.extend(((str(i)+"-"+str('00'))).split())
        elif(i==0):
            period.extend((str('00')+"-"+str(i+1)).split())
        else:
            period.extend((str(i)+"-"+str(i+1)).split())
            
    df['time_period']=period
        # print(df.head())
        
    return df

# print(preprocess(data))