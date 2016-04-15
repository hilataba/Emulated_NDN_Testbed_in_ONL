#!/usr/bin/python2

import os
import shutil
import glob
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


total = len(sys.argv)
if total < 2:
  sys.exit("usage: python parseResults.py <expName>")

expName = sys.argv[1]
outDirectory = '/Users/user/Documents/repo/papers/forwardingStrategies/NetworkRetransmission/results/'+expName+'/'

if not os.path.exists(outDirectory):
  os.makedirs(outDirectory)

parsedList = []
itr_time_list = [0]
itr = 0
#for filename in glob.glob(os.path.join('/Users/user/Documents/repo/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data', '*.csv')):
for filename in glob.glob(os.path.join('/Users/user/Documents/repo/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/'+expName+'/', '*.csv')):
  print 'copy file: ' + filename
  shutil.copy(filename, outDirectory)
  inputfile = open(filename)
  text = inputfile.readlines()[0:]
  text = [line[:-1] for line in text]
  # get line and iteration
  name = text[0]
  itr_time = text[1]
  if itr_time not in itr_time_list:
    itr += 1
    itr_time_list.append(itr_time)
  else:
    itr = itr_time_list.index(itr_time)
  
  #get the first row of data
  prevRow = text[3].split(',')
  
  #go over the list to create the data structure
  for item in text[4:]:
    currRow = item.split(',')
    pktRate = (int(currRow[1]) - int(prevRow [1])) / (float(currRow[0]) - float(prevRow [0]))
    prevRow = currRow

#parsedList.append([currRow[0], pktRate, name, itr])
#if [round(float(currRow[0]),1), pktRate, name, itr] in parsedList:
#     print "DUPLICATE: "
#     print [round(float(currRow[0]),1), pktRate, name, itr]
#   else:
    parsedList.append([(currRow[0])[:-2], pktRate, name, itr])

#df = pd.DataFrame.from_dict(parsedList,orient='columns')
df = pd.DataFrame(parsedList, columns = ['time', 'pktRate', 'name', 'itr'])
#df.columns = ['time', 'pktRate', 'name', 'itr']
df[['time']] = df[['time']].astype(float)
df = df.sort_values(['time','name'])
df.index = pd.Series(range(len(df)))
df.to_csv(outDirectory+'/all.csv')


#print df.groupby(['time', 'name'])
#remove rows without full info
#for row in df.iterrows():
  # make the same row exist for all itrs
# print row['time']

#print df.index
#print df

#sns.set(style="darkgrid")

# Plot the response with standard error
#plot = sns.tsplot(data=df[:200], time="timepoint", unit="itr", condition="name", value="pktRate")
plot = sns.tsplot(data=df, time = 'time', unit='itr', value='pktRate', condition = 'name')
fig = plot.get_figure()
fig.savefig(outDirectory+'/'+expName+'.jpg')



#df1 = pd.DataFrame(df.values)
#df1 = pd.DataFrame(df.values, columns = ['time', 'pktRate', 'name', 'itr'])
#df['time'] = pd.Series(list(range(len(df))))
#fig2 = df.plot(x='time', y='pktRate')
plt.show()
#fig2.savefig("test.jpg")




