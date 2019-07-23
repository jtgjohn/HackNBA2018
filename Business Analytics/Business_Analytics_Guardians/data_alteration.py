import pandas as pd 

#loading data
df = pd.read_csv('training_set.csv', encoding = 'latin1') 

#might want to save for later
description = df['Description']

#Dealing with Create Date Data
df['Created'] = pd.to_datetime(df['Created'])
#month variable
df['Month'] = df['Created'].dt.month_name()

#weekday variable
df['Weekday'] = df['Created'].dt.day_name()

#time variable (in seconds)
df['Seconds'] = df['Created'].dt.hour * 3600 + df['Created'].dt.minute * 60 + df['Created'].dt.second
df = df.drop(['Created'], axis = 1, inplace = False)

export_csv = df.to_csv(r'training_altered.csv', index = None, header = True)