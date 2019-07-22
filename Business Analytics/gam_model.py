import pandas as pd 
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from patsy import dmatrix
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

#time variable (in seconds)
df['Seconds'] = df['Created'].dt.hour * 3600 + df['Created'].dt.minute * 60 + df['Created'].dt.second

#Cleaning the data
df = df.drop(['Description'], axis = 1, inplace = False)
df = df.drop(['Created'], axis = 1, inplace = False)
df = df.drop(['Month'], axis = 1, inplace = False)


#Dealing with categorical variable 'Type': dropping one dummy to prevent multicolinearity
df = pd.get_dummies(df, drop_first = True) 
df = df.join(month_dummy)

X = df

seconds_spline = X['Seconds']
followers_spline = X['Followers at Posting']

transformed_seconds = dmatrix("bs(train1, df = 5, degree=3, include_intercept = False)", {"train1": seconds_spline}, return_type='dataframe')
transformed_followers = dmatrix("bs(train2, df = 5, degree=3, include_intercept = False)", {"train2": followers_spline}, return_type='dataframe')

transformed_seconds = transformed_seconds.drop(['Intercept'], axis=1, inplace=False)

X_spline = X.join(transformed_seconds)
X_spline=X_spline.join(transformed_followers)

X_spline = X_spline.drop(['Seconds'], axis = 1, inplace=False)
X_spline = X_spline.drop(['Followers at Posting'], axis = 1, inplace=False)
y = X_spline.iloc[:, 0]
x = X_spline.iloc[:, 1:30]
model = sm.OLS(y, x).fit()
print(model.summary())











