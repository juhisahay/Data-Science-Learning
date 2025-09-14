# Youtube Tutorial: https://youtu.be/7SRcYdd9JcY?si=BfSiQptk9fMkYKTk
# credit for code goes to ___Rob Mulla____

# %%
import pandas as pd
import matplotlib.pylab as plt
import datetime
from itertools import cycle
import numpy as np


pd.set_option("display.max_rows", 500)  # Why columns? Dataset has 5 rows

# For plotting

plt.style.use("ggplot")
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
color_cycle = cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])

# Load in the Dataset and Parse Tweet Text

tweets = pd.read_csv(
    "C:/Users/aksah/Documents/code/Data-Science-Learning/datasets/wordle-tweets/tweets.csv"
)
# tweets.shape tells size of dataset in kaggle notebook
tweets.tail()


def process_tweets(tweets):
    tweets["tweet_datetime"] = pd.to_datetime(
        tweets["tweet_date"]
    )  # changed format to datetime
    tweets["tweet_date"] = tweets["tweet_datetime"].dt.date  # takes only the date
    tweets["wordle_id"] = tweets["tweet_text"].str[:10]
    tweets["n_attempts"] = tweets["tweet_text"].str[11].astype("int")
    tweets["id"] = tweets["tweet_text"].str[7:10].astype("int")

    # truncate to Jan-Feb dates only
    March = datetime.date(2022, 3, 1)
    tweets = tweets[tweets["tweet_date"] < March]

    return tweets


tweets = process_tweets(tweets)

# How many tweets do we have for each date
tweets.groupby("tweet_date").size().plot(
    figsize=(10, 5), title="World Tweets By Day", color=color_pal[2], lw=5
)
plt.show()  # running a plot

# Number of Attempts analysis by Wordle ID
# unstack() - makes number of attempts our columns instead of a multi index
number_of_attempts_graph = (
    tweets.groupby("wordle_id")["n_attempts"]
    .value_counts()
    .unstack()
    .style.background_gradient(axis=1)
)

# How many attempts does it usually take to solve?
ax = (
    tweets["n_attempts"]
    .value_counts()
    .sort_index()
    .plot(
        figsize=(10, 5),
        kind="barh",
        title="Number of Wordle Attempts",
        edgecolor="black",
    )
)
ax.set_xlabel("Number of Tweets")
ax.set_ylabel("Number of Attempts Solved in")
plt.show()

# Parse Tweet Text
# Make dark squares consistent across all wordles
tweets["tweet_text"] = tweets["tweet_text"].str.replace("⬜", "⬛")  # how to get color


# Plot Results by Attempt - Wordle Average Results by Guess Number
""" place code here """


# Average number of guesses per wordle ID - Do it yourself
def guessesPerID():
    # group by ID
    tweets["wordle_id"] = tweets["wordle_id"].str[8:11]
    Avg = tweets.groupby("wordle_id")["n_attempts"].mean()

    # Axes
    fig, axs = plt.subplots(figsize=(10, 5))
    axs.set_xlabel("Wordle ID")
    axs.set_ylabel("Average Number of Attempts")
    axs.set_title("Average Attempts per Wordle")

    # Line graph
    Avg.plot(kind="line", color="blue", marker="o", ax=axs)

    # Plot horizontal average line
    plt.axhline(y=np.nanmean(Avg), color="red", linestyle="--", label="overall average")
    plt.legend(loc="upper right")

    plt.show()


guessesPerID()

# Plot Letter Analysis- Most Common Correct First Guess Letters
""" place code here"""

# User participation


# %%
