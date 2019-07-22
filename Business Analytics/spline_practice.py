from patsy import dmatrix
from sklearn.model_selection import KFold
import numpy as np
import pandas as pd 
import statsmodels.api as sm
import matplotlib.pyplot as plt 


def spline_transform(seconds, followers, dummies):
	transformed_seconds = dmatrix("cr(train_seconds, df = 10)", {"train_seconds": seconds}, return_type='dataframe')
	transformed_followers = dmatrix("cr(train_followers, df = 10)", {"train_followers": followers}, return_type='dataframe')
	transformed_followers = transformed_followers.drop(['Intercept'], axis=1, inplace=False)
	X = dummies.join(transformed_seconds)
	X = X.join(transformed_followers)
	return X


#loading data
df = pd.read_csv('training_set.csv', encoding = 'latin1') 

#altering data
df['Created'] = pd.to_datetime(df['Created'])
df['Seconds'] = df['Created'].dt.hour * 3600 + df['Created'].dt.minute * 60 + df['Created'].dt.second
df['Month'] = df['Created'].dt.month_name()

#quantitative regressors
seconds = df['Seconds']
followers = df['Followers at Posting']
y = df['Engagements']

#Dealing with Dummies 
type_dummy = pd.get_dummies(df['Type'], drop_first=True)
month_dummy = pd.get_dummies(df['Month'], drop_first = True)
dummies = type_dummy.join(month_dummy)

X = spline_transform(seconds, followers, dummies)
fit = sm.OLS(y, X).fit()	
print(fit.summary())

#Cross Validation 
MAPE_cv = [] #mean absolute percentage error
cv = KFold(n_splits = 10, shuffle=True)
for train_index, test_index in cv.split(X, y):
    n = len(test_index)
    seconds_train, seconds_test = seconds.iloc[train_index], seconds.iloc[test_index]
    followers_train, followers_test = followers.iloc[train_index], followers.iloc[test_index]
    dummies_train, dummies_test = dummies.iloc[train_index], dummies.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    X_train = spline_transform(seconds_train, followers_train, dummies_train)
    results = sm.OLS(y_train, X_train).fit()
    X_test = spline_transform(seconds_test, followers_test, dummies_test)
    predictions = results.predict(X_test)
    MAPE_cv.append(1/n * sum(abs((y_test - predictions)/y_test)))
    

print(np.mean(MAPE_cv))






#FOR PLOTTING 
#followersp = np.linspace(followers.min(), followers.max(), 200)

#regressors = dmatrix("cr(xp, df = 5)", {"xp": followersp}, return_type='dataframe')

#regressors = regressors.join(type_dummy)

#pred = fit.predict(regressors)

#plt.scatter(df['Followers at Posting'], df['Engagements'], facecolor='None', edgecolor='k', alpha=0.1)
#plt.scatter(followersp, pred, color='g')
#plt.xlabel('Followers')
#plt.ylabel('Engagements')
#plt.show()