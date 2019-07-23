import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def norm(x):
	x_stats = x.describe()
	x_stats = x_stats.transpose()
	return (x - x_stats['mean']) / x_stats['std']

def alter_data(dataframe, teams, players):
  n = len(dataframe)
  df = dataframe.copy()

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
  return X



teams = ["@raptors", "@warriors", "@nuggets", "@okcthunder", "@pelicansnba", "@dallasmavs", "@hornets", "@lakers", "@nyknicks", "@timberwolves", "@laclippers", "@orlandomagic", "@pacers", "@cavs", "@houstonrockets", "@brooklynnets", "@suns", "@spurs", "@utahjazz", "@celtics", "@atlhawks", "@detroitpistons", "@chicagobulls", "@sixers", "@bucks", "@washwizards", "@miamiheat", "@memgrizz", "@trailblazers", "@sacramentokings"]
players = ["@kingjames", "@stephencurry30", "@kyrieirving", "@dwyanewade", "@russwest44", "@cp3", "@jharden13", "@ygtrece", "@carmeloanthony", "@klaythompson", "@damianlillard"]

#loading data
df_training = pd.read_csv('training_set.csv', encoding = 'latin1') 
df_holdout = pd.read_csv('holdout_set.csv', encoding = 'latin1')

X = alter_data(df_training, teams, players)
y = df_training['Engagements']

X_holdout = alter_data(df_holdout, teams, players)

normed_X = norm(X)
normed_X_holdout = norm(X_holdout)


def build_model():
  model = keras.Sequential([
    layers.Dense(64, activation=tf.nn.relu, input_shape=[len(X.keys())]),
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
  normed_X, y,
  epochs=EPOCHS, validation_split = 0.2, verbose=0,
  callbacks=[PrintDot()])

predictions = model.predict(normed_X_holdout).flatten()
engagements_holdout = pd.DataFrame(data=predictions, columns=['Engagements'])

df_holdout['Engagements'] = engagements_holdout
export_csv = df_holdout.to_csv(r'holdout_set_Guardians.csv', index = None, header=True)














