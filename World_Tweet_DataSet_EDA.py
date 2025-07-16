# Youtube Tutorial: https://youtu.be/7SRcYdd9JcY?si=BfSiQptk9fMkYKTk
# credit for code goes to _______

# %%
import pandas as pd
import matplotlib.pylab as plt
import datetime
import re

pd.set_option("display.max_rows", 500)  # Why columns? Dataset has 5 rows

# For plotting
from itertools import cycle

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

# Number of Attempts analysis by Worlde ID
# unstack() - makes number of attempts our columns instead of a multi index
tweets.groupby("wordle_id")["n_attempts"].value_counts().unstack()
# .style.background_gradient(axis=1)

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


def parse_tweet_text(tweets):
    for n in range(6):
        n += 1  # parse out what the boxes look like for each attempt
        tweets[f"has_guess{n}"] = (
            tweets["tweet_text"]
            .str.split("\n")
            .str[n + 1]
            .str.contains("|".join(["🟨", "⬛", "🟩"]))
            .fillna(False)
        )

        # Parse out the tweet text
        tweets.loc[tweets[f"has_guess{n}"], f"guess{n}"] = (
            tweets["tweet_text"].str.split("\n").str[n + 1].str[:5]
        )

        # Count number cprrect, misplaced, and incorrect
        tweets.loc[tweets[f"has_guess{n}"], f"guess{n}_incorrect"] = tweets[
            f"guess{n}"
        ].str.count("⬛")

        tweets.loc[tweets[f"has_guess{n}"], f"guess{n}_wrong_spot"] = tweets[
            f"guess{n}"
        ].str.count("🟨")

        tweets.loc[tweets[f"has_guess{n}"], f"guess{n}_correct"] = tweets[
            f"guess{n}"
        ].str.count("🟩")

        tweets.loc[tweets[f"guess{n}_correct"] == 6, "final_guess"] = n

        return tweets


tweets = parse_tweet_text(tweets)

# Keep additional tweet text
tweets["additional_text"] = (
    tweets.loc[~tweets["tweet_text"].str.split("\n").str[-1].str.contains("🟩")][
        "tweet_text"
    ]
    .str.split("\n")
    .str[-1]
)


# Plot results by Attempt
fig, axs = plt.subplots(1, 3, figsize=(12, 5), sharex=True)

for i, x in enumerate(["_correct", "_wrong_spot", "_incorrect"]):
    col_subset = [c for c in tweets.columns if x in c]
    guess_avg = tweets[col_subset].mean()
    guess_avg.index = [f"Guess {i + 1}" for i in range(6)]
    guess_avg.sort_index(ascending=False).plot(
        kind="barh",
        title=f"{x.strip('_').replace('_', ' ').title()}",
        ax=axs[i],
        color=color_pal[i + 1],
    )
    axs[i].set_xlabel("Average Letters")
fig.suptitle("Wordle Average Results by Guess Number", fontsize=18)
plt.tight_layout()
plt.show()

# Letter Analysis
first_guess_correct = []
for i, d in tweets.dropna(subset=["answer"]).iterrows():
    example_text = d["guess1"]
    example_solution = d["answer"]
    results = [x.span()[0] for x in re.finditer("🟩", example_text)]
    first_guess_letters = [example_solution[i] for i in results]
    first_guess_correct += first_guess_letters

pd.Series(first_guess_correct).value_counts(ascending=True).plot(
    kind="barh",
    figsize=(10, 5),
    title="Most Common Correct First Guess Letters",
    edgecolor="black",
    color=color_pal[5],
)
plt.show()
# %%
