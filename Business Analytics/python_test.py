import pandas as pd 

teams = ["@raptors", "@warriors", "@nuggets", "@okcthunder", "@pelicansnba", "@dallasmavs", "@hornets", "@lakers", "@nyknicks", "@timberwolves", "@laclippers", "@orlandomagic", "@pacers", "@cavs", "@houstonrockets", "@brooklynnets", "@suns", "@spurs", "@utahjazz", "@celtics", "@atlhawks", "@detroitpistons", "@chicagobulls", "@sixers", "@bucks", "@washwizards", "@miamiheat", "@memgrizz", "@trailblazers", "@sacramentokings"]
allstars = ["LeBron", "@kingjames", "@jharden13", "@kyrieirving", "kawhi", "@antdavis23","@bensimmons","@damianlillard","@dwyanewade","@karltowns","@klaythompson","@giannis_an34","@stephencurry30","@joelembiid","@ygtrece","Kemba","@blakegriffin23","@dloading","Dirk", "@swish41", "Jokic","oladipo","@russwest44","@kporzee","@johnwall", "@demar_derozan","@money23green","@easymoneysniper","@jimmybutler","@isaiahthomas","@carmeloanthony"]

df_holdout = pd.read_csv('holdout_set.csv', encoding = 'latin1')
print(df_holdout.head(5))