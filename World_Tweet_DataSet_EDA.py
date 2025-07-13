# Youtube Tutorial: https://youtu.be/7SRcYdd9JcY?si=BfSiQptk9fMkYKTk 
# credit for code goes to _______

#%% 
import itertools 
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import re

pd.set_option("display.max_columns", 500)

# For plotting
from itertools import cycle

plt.style.use("ggplot")
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
color_cycle = cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])

# Load in the Dataset and Parse Tweet Text 

tweets = pd.read_csv("DATA-SCIENCE-LEARNING/datasets/tweets.csv")

# tweets.shape tells size of dataset in kaggle notebook
def process_tweets(tweets):
    tweets["tweet_datetime"] = pd.to_datetime(tweets['tweet_date']) # changed format to datetime
    tweets["tweet_date"] = tweets["tweet_datetime"].dt.date # takes only the date
    tweets["wordle_id"] = tweets["tweet_text"].str[:10]
    tweets["n_attempts"] = tweets["tweet_text"].str[11].astype("int")
    tweets["id"] = tweets["tweet_text"].str[7:10].astype("int")
    return tweets

tweets = process_tweets(tweets)

# How many tweets do we have for each date
tweets["tweet_date"].value_counts(). \
    plot(figsize= (10, 5), title = "World Tweets By Day", 
         color = color_pal[2], lw=5)
plt.show() # running a plot
# %%
