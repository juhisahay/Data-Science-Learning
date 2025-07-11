# Youtube Tutorial: https://youtu.be/7SRcYdd9JcY?si=BfSiQptk9fMkYKTk 

import itertools 
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import re

pd.set_option("max_columns", 500)

# For plotting
from itertools import cycle

plt.style.use("ggplot")
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
color_cycle = cycle(plt.rcParams["axes,prop_cycle"].bykey()["color"])

# Load in the Dataset

tweets = pd.read_csv("tweets.csv")

# tweets.shape tells size of dataset in kaggle notebook
tweets["tweet_date"] = pd.to_datetime
