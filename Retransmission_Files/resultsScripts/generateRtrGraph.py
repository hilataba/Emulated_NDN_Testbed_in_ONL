#!/usr/bin/python2

"""
  Timeseries from DataFrame
  =========================
  
  """
import matplotlib.pyplot as plt

import seaborn as sns
sns.set(style="darkgrid")

# Load the long-form example gammas dataset
#gammas = sns.load_dataset("../UIUC")
gammas = sns.load_dataset("gammas")

# Plot the response with standard error
plot = sns.tsplot(data=gammas, time="timepoint", unit="subject",
           condition="ROI", value="BOLD signal")
fig = plot.get_figure()
fig.savefig("output.jpg")
