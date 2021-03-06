import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def norm(x):
	x_stats = x.describe()
	x_stats = x_stats.transpose()
	return (x - x_stats['mean']) / x_stats['std']

teams = ["@raptors", "@warriors", "@nuggets", "@okcthunder", "@pelicansnba", "@dallasmavs", "@hornets", "@lakers", "@nyknicks", "@timberwolves", "@laclippers", "@orlandomagic", "@pacers", "@cavs", "@houstonrockets", "@brooklynnets", "@suns", "@spurs", "@utahjazz", "@celtics", "@atlhawks", "@detroitpistons", "@chicagobulls", "@sixers", "@bucks", "@washwizards", "@miamiheat", "@memgrizz", "@trailblazers", "@sacramentokings"]
players = ["@kingjames", "@stephencurry30", "@kyrieirving", "@dwyanewade", "@russwest44", "@cp3", "@jharden13", "@ygtrece", "@carmeloanthony", "@klaythompson", "@damianlillard"]

#loading data
df = pd.read_csv('training_set.csv', encoding = 'latin1') 
n = len(df)

#altering data
df['Created'] = pd.to_datetime(df['Created'])
df['Seconds'] = df['Created'].dt.hour * 3600 + df['Created'].dt.minute * 60 + df['Created'].dt.second
df['Month'] = df['Created'].dt.month_name()
df['Weekday'] = df['Created'].dt.day_name()

#Top Team Instagram Followers
team_mentions = np.zeros((n, len(teams)))
row_counter = 0
for index, row in df.iterrows():
	for team in teams:
		if str(team) in str(row['Description']):
			team_mentions[row_counter, teams.index(team)] = 1
		else: 
			continue
	row_counter += 1
team_dummy = pd.DataFrame(data=team_mentions, columns=teams)

#Top Player Instagram Followers
player_mentions = np.zeros((n, len(players)))
row_counter = 0
for index, row in df.iterrows():
	for player in players:
		if str(player) in str(row['Description']):
			player_mentions[row_counter, players.index(player)] = 1
		else:
			continue
	row_counter += 1
player_dummy = pd.DataFrame(data=player_mentions, columns=players)


#quantitative regressors
seconds = df['Seconds']
followers = df['Followers at Posting']
y = df['Engagements']

#Dealing with Dummies 
type_dummy = pd.get_dummies(df['Type'])
month_dummy = pd.get_dummies(df['Month'])
weekday_dummy = pd.get_dummies(df['Weekday'])
dummies = type_dummy.join(month_dummy)
dummies = dummies.join(weekday_dummy)
dummies = dummies.join(player_dummy)
dummies = dummies.join(team_dummy)

X = dummies.join(seconds)
X = X.join(followers)

dataset = X.join(y)
train_dataset = dataset.sample(frac=0.8, random_state=42)
test_dataset = dataset.drop(train_dataset.index)
train_label = train_dataset.pop('Engagements')
test_label = test_dataset.pop('Engagements')

normed_train_dataset = norm(train_dataset)
normed_test_dataset = norm(test_dataset)


def build_model():
  model = keras.Sequential([
    layers.Dense(64, activation=tf.nn.relu, input_shape=[len(train_dataset.keys())]),
    layers.Dense(64, activation=tf.nn.relu),
    layers.Dense(1)
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mean_squared_error',
                optimizer=optimizer,
                metrics=['mean_absolute_percentage_error'])
  return model

model = build_model()

# Display training progress by printing a single dot for each completed epoch
class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

EPOCHS = 1000

history = model.fit(
  normed_train_dataset, train_label,
  epochs=EPOCHS, validation_split = 0.2, verbose=0,
  callbacks=[PrintDot()])

test_predictions = model.predict(normed_test_dataset).flatten()
test_labelnp = test_label.to_numpy()

print("Predictions:")
print(test_predictions[0:3])
print(type(test_predictions))
print("Actual: ")
print(test_labelnp[0:3])
print(type(test_labelnp))

MAPE = sum(abs((test_predictions - test_labelnp)/test_labelnp)) * 1/n

print("Mean average percentage error: " + str(MAPE))




