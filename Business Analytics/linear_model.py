import pandas as pd 
import numpy as np
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
df = df.drop(['Followers at Posting'], axis = 1, inplace = False)


#Dealing with categorical variable 'Type': dropping one dummy to prevent multicolinearity
df = pd.get_dummies(df, drop_first = True) 
#df = df.join(Weekday_dummy)
df = df.drop(['Type_Photo'], axis = 1, inplace=False)

#OLS (and probably better models in the future)
y = df.iloc[:, 0]
X = df.iloc[:, 1:21]
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print(model.summary())

#cross validation 
MAPE = [] #mean absolute percentage error
cv = KFold(n_splits = 10, shuffle=True)
for train_index, test_index in cv.split(X, y):
    n = len(test_index)
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    results = sm.OLS(y_train, X_train).fit()
    predictions = results.predict(X_test)
    MAPE.append(1/n * sum(abs((y_test - predictions)/y_test)))
    
print(np.mean(MAPE))









    


