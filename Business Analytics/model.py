import pandas as pd 
import statsmodels.api as sm
from sklearn.model_selection import KFold

#loading data
df = pd.read_csv('training_set.csv', encoding = 'latin1') 

#might want to save for later
description = df['Description']


#Dealing with Create Date Data
df['Created'] = pd.to_datetime(df['Created'])
#month variable
df['Month'] = df['Created'].dt.month_name()
month_dummy = pd.get_dummies(df['Month'], drop_first = True)
print(month_dummy)
#weekday variable
df['Weekday'] = df['Created'].dt.day_name()
Weekday_dummy = pd.get_dummies(df['Weekday'], drop_first = True)

#time variable (in seconds)
df['Seconds'] = df['Created'].dt.hour * 3600 + df['Created'].dt.minute * 60 + df['Created'].dt.second

#Cleaning the data
#df = df.drop(['Engagements'], axis = 1, inplace = False)
df = df.drop(['Description'], axis = 1, inplace = False)
df = df.drop(['Created'], axis = 1, inplace = False)
df = df.drop(['Weekday'], axis = 1, inplace = False)

#Dealing with categorical variable 'Type': dropping one dummy to prevent multicolinearity
df = pd.get_dummies(df, drop_first = True) 
df = df.join(Weekday_dummy)
#print(df)

#OLS (and probably better models in the future)
Y = df.iloc[:, 0]
X = df.iloc[:, [1,8]]
X = sm.add_constant(X)
results = sm.OLS(Y, X).fit()
#print(results.summary())

#cross validation 
#test#










    


