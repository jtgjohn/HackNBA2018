from sklearn.model_selection import KFold
from sklearn.linear_model import Ridge
from patsy import dmatrix
import pandas as pd 
import numpy as np
import statsmodels.api as sm

def spline_transform(seconds, followers, dummies):
	transformed_seconds = dmatrix("cr(train_seconds, df = 10)", {"train_seconds": seconds}, return_type='dataframe')
	transformed_followers = dmatrix("cr(train_followers, df = 10)", {"train_followers": followers}, return_type='dataframe')
	transformed_followers = transformed_followers.drop(['Intercept'], axis=1, inplace=False)
	X = dummies.join(transformed_seconds)
	X = X.join(transformed_followers)
	return X

teams = ["@raptors", "@warriors", "@nuggets", "@okcthunder", "@pelicansnba", "@dallasmavs", "@hornets", "@lakers", "@nyknicks", "@timberwolves", "@laclippers", "@orlandomagic", "@pacers", "@cavs", "@houstonrockets", "@brooklynnets", "@suns", "@spurs", "@utahjazz", "@celtics", "@atlhawks", "@detroitpistons", "@chicagobulls", "@sixers", "@bucks", "@washwizards", "@miamiheat", "@memgrizz", "@trailblazers", "@sacramentokings"]
allstars = ["LeBron", "@kingjames", "@jharden13", "@kyrieirving", "kawhi", "@antdavis23","@bensimmons","@damianlillard","@dwyanewade","@karltowns","@klaythompson","@giannis_an34","@stephencurry30","@joelembiid","@ygtrece","@_kw15","@blakegriffin23","@dloading","Dirk", "@swish41", "Jokic","oladipo","@russwest44","@kporzee","@johnwall", "@demar_derozan","@money23green","@easymoneysniper","@jimmybutler","@isaiahthomas","@carmeloanthony"]

#loading data
data = pd.read_csv('training_set.csv', encoding = 'latin1') 

df = data.copy()

n = len(df)

team_dummy = np.zeros((n, len(teams)))
all_star_dummy = np.zeros((n, len(allstars)))


#teams
df['Description'] = df['Description'].astype(str)

row_counter = 0
for index, row in df.iterrows():
	for team in teams: 
		if team in row['Description']:
			team_dummy[row_counter, teams.index(team)] = 1
		else: 
			continue
	row_counter += 1
	
team_mentions = pd.DataFrame(data=team_dummy, columns=teams)

#all_stars
row_counter = 0
for index, row in df.iterrows():
	for allstar in allstars: 
		if allstar in row['Description']:
			all_star_dummy[row_counter, allstars.index(allstar)] = 1
		else:
			continue
	row_counter += 1
	
all_star_mentions = pd.DataFrame(data=all_star_dummy, columns=allstars)	

#altering data
df['Created'] = pd.to_datetime(df['Created'])
df['Seconds'] = df['Created'].dt.hour * 3600 + df['Created'].dt.minute * 60 + df['Created'].dt.second
df['Month'] = df['Created'].dt.month_name()
df['Weekday'] = df['Created'].dt.day_name()


#quantitative regressors
seconds = df['Seconds']
followers = df['Followers at Posting']
y = df['Engagements']

#Dealing with Dummies 
type_dummy = pd.get_dummies(df['Type'], drop_first=True)
month_dummy = pd.get_dummies(df['Month'], drop_first = True)
weekday_dummy = pd.get_dummies(df['Weekday'], drop_first = True)
dummies = type_dummy.join(month_dummy)
dummies = dummies.join(weekday_dummy)
dummies = dummies.join(team_mentions)
dummies = dummies.join(all_star_mentions)

X = dummies.join(seconds)
X = X.join(followers)
X = sm.add_constant(X)

fit = sm.OLS(y, X).fit()
print(fit.summary())

#cross validation - linear regression
MAPE_linear = [] #mean absolute percentage error
cv = KFold(n_splits = 10, shuffle=True)
for train_index, test_index in cv.split(X, y):
    a = len(test_index)
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    results = sm.OLS(y_train, X_train).fit()
    predictions = results.predict(X_test)
    MAPE_linear.append(1/a * sum(abs((y_test - predictions)/y_test)))
    
print("Linear regression: " + str(np.mean(MAPE_linear)))
#higher cross validation MAPE even with high R square might be a case of overfitting

#cross validation - ridge regression 
MAPE_ridge = [] #mean absolute percentage error
cv = KFold(n_splits = 10, shuffle=True)
for train_index, test_index in cv.split(X, y):
    a = len(test_index)
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    fit_ridge = Ridge(alpha=30)
    fit_ridge.fit(X_train, y_train)
    predictions = fit_ridge.predict(X_test)
    MAPE_ridge.append(1/a * sum(abs((y_test - predictions)/y_test)))

print("Ridge regression: " + str(np.mean(MAPE_ridge)))

#Cross Validation - spline regression
MAPE_spline = [] #mean absolute percentage error
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
    MAPE_spline.append(1/n * sum(abs((y_test - predictions)/y_test)))
    

print("Spline Regression: " + str(np.mean(MAPE_spline)))

print(data.head(5))

    





