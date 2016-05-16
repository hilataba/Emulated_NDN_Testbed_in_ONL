#!/usr/bin/python2

import os
import shutil
import glob
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import seaborn as sns
import errno
import subprocess
import csv
import statistics
from numpy import matrix

from collections import deque

multiPathResultsDf = pd.DataFrame(columns = ['title', 'sent', 'received', 'loss', 'rtt','strategy'])

multiProducersResultsDf = pd.DataFrame(columns = ['title', 'sent', 'received_orange', 'received_kisti', 'loss', 'rtt','strategy','dropRate','total_sent_wash_u'])

multiPathResults = {
'title':{'b2':[],'b3':[],'n':[], 'n2':[]},
'sent':{'b2':[],'b3':[],'n':[], 'n2':[]},
'received':{'b2':[],'b3':[],'n':[], 'n2':[]},
'loss':{'b2':[],'b3':[],'n':[], 'n2':[]},
'rtt':{'b2':[],'b3':[],'n':[], 'n2':[]}
}

def grepData(name, param, file, outDirectory):
  
  cmd = 'grep -A 6 Name='+name+ ', ' +outDirectory+file+' | grep "'+param+'" | cut -d= -f2 | cut -d" " -f2'
  ReceivedInterests = subprocess.check_output(['bash','-c', cmd])
  
  return ReceivedInterests;

def copyDirectory(src, dest):
  try:
    shutil.copytree(src, dest)
    # Directories are the same
  except shutil.Error as e:
    print('Directory not copied. Error: %s' % e)
  # Any error saying that the directory doesn't exist
  except OSError as e:
    print('Directory not copied. Error: %s' % e)

def plotTimeCounters(expName, outDirectory):
  #outDirectory = destDir+expName
  sns.set_style("white")
  sns.set_context("paper", font_scale=2.1, rc={"lines.linewidth": 2.5})
  
  parsedList = []
  itr_time_list = [0]
  itr = 0
    #for filename in glob.glob(os.path.join(outDirectory+expName+'/', '*.csv')):
  for filename in glob.glob(os.path.join(outDirectory, '*.csv')):
    if ('/all.csv' in filename):
      print "NEED TO SKIP"
      continue
    print 'parse file: ' + filename
    #shutil.copy(filename, outDirectory)
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
      parsedList.append([(currRow[0])[:-2], pktRate, name, itr])

  df = pd.DataFrame(parsedList, columns = ['time', 'pktRate', 'Link', 'itr'])
  df[['time']] = df[['time']].astype(float)
  df = df.sort_values(['time','Link'])
  df = df.drop_duplicates(['time','Link'], keep='first')
  df.index = pd.Series(range(len(df)))
  df.to_csv(outDirectory+'/all.csv')
  
  
  nameArr = expName.split("_")
  if(nameArr[4]=='b2'):
    strategy = "best-route"
  elif (nameArr[4]=='b3'):
    strategy = "best-route-r"
  elif (nameArr[4]=='n'):
    strategy = "ncc"
  elif (nameArr[4]=='n2'):
    strategy = "ncc-r"
  
  list_of_values = ["FROM_CLIENT", "TO_CLIENT" ,"TO_KISTI", ]
  # Plot the response with standard error
  sortedDF = df[df['Link'].isin(list_of_values)]
  sortedDF.Link[sortedDF.Link=='FROM_CLIENT']='Consumer TX'
  sortedDF.Link[sortedDF.Link=='TO_CLIENT']='Consumer RX'
  sortedDF.Link[sortedDF.Link=='TO_KISTI']='Producer RX'
  plot = sns.tsplot(data=sortedDF, time = 'time', unit='itr', value='pktRate', condition = 'Link')
  plot.set_ylabel('Packet Rate (Interests/Second)')
  plot.set_xlabel('Time (seconds)')
  plot.set_title(strategy)
  fig = plt.figure()
  fig = plot.get_figure()
  
  
  list_of_values = ["TO_URJC", "TO_VERISIGN" ,"TO_UIUC", "TO_UM" ]
  # Plot the response with standard error
  sortedDF = df[df['Link'].isin(list_of_values)]
  sortedDF.Link[sortedDF.Link=='TO_URJC']='TO URJC'
  sortedDF.Link[sortedDF.Link=='TO_VERISIGN']='TO VERISIGN'
  sortedDF.Link[sortedDF.Link=='TO_UIUC']='TO UIUC'
  sortedDF.Link[sortedDF.Link=='TO_UM']='TO UM'
  plot = sns.tsplot(data=sortedDF, time = 'time', unit='itr', value='pktRate', condition = 'Link')
  plot.set_ylabel('Packet Rate (Interests/Second)')
  plot.set_xlabel('Time (seconds)')
  plot.set_title(strategy)
  fig = plt.figure()
  fig = plot.get_figure()
  plt.show()
  fig.savefig(outDirectory+'/'+expName+'_WU.jpg')
  return

def parseData(expName, outDirectory):
  global multiPathResultsDf
  global multiProducersResultsDf
  if "MultipilePaths_drop" in expName:
    
    name = expName.split("_")
    date = name[0]
    title = name[2]
    strategy = name[4]
    itr = name[5]
    
    multiPathResults['title']=title
    
    serverReceivedInterests = grepData("/ndn/kr/re/kisti/host", "Total Interests Received", "ndn-traffic-server.log", outDirectory)
    
    clientSentInterests = grepData("/ndn/kr/re/kisti/host", "Total Interests Sent", "ndn-traffic.log", outDirectory)
  
    TotalInterestLoss = grepData("/ndn/kr/re/kisti/host", "Total Interest Loss", "ndn-traffic.log", outDirectory)
    
    AverageRoundTripTime = grepData("/ndn/kr/re/kisti/host", "Average Round Trip Time", "ndn-traffic.log", outDirectory)
    
    startCountersCmd = 'cat '+outDirectory+'nfd-status-wustl-rtr_start | grep out= | cut -d{ -f4 | cut -d" " -f1 | cut -di -f1'
    finalCountersCmd = 'cat '+outDirectory+'nfd-status-wustl-rtr_final | grep out= | cut -d{ -f4 | cut -d" " -f1 | cut -di -f1'
    startCounters = subprocess.check_output(['bash','-c', startCountersCmd])
    finalCounters = subprocess.check_output(['bash','-c', finalCountersCmd])
    
    startCounters = startCounters.split('\n')
    startCounters = startCounters[:-1]
    startCounters = matrix([int(i) for i in startCounters])
    
    finalCounters = finalCounters.split('\n')
    finalCounters = finalCounters[:-1]
    finalCounters = matrix([int(i) for i in finalCounters])
    
    diff = (finalCounters - startCounters)
    totalWustl=matrix.sum(diff)

    multiPathResultsDf = multiPathResultsDf.append({'title':title, 'sent':int(clientSentInterests), 'received':int(serverReceivedInterests),'loss':float(TotalInterestLoss[:-2]),'rtt':float(AverageRoundTripTime[:-3]), 'strategy':strategy, 'total_sent_wash_u':totalWustl}, ignore_index=True)
  
  elif "MultipileProducer" in expName:
    name = expName.split("_")
    date = name[0]
    title = name[2]
    dropRate = name[3]
    strategy = name[5]
    itr = name[6]
  
    orang_serverReceivedInterests = int(grepData("/ndn/distributedDB/producer/host", "Total Interests Received", "ndn-traffic-server-orange_1", outDirectory))
    
    orang_serverReceivedInterests += int(grepData("/ndn/distributedDB/producer/host", "Total Interests Received", "ndn-traffic-server-orange_2", outDirectory))
  
    kisti_serverReceivedInterests = int(grepData("/ndn/distributedDB/producer/host", "Total Interests Received", "ndn-traffic-server-kisti", outDirectory))
    
    clientSentInterests = grepData("/ndn/distributedDB/producer/host", "Total Interests Sent", "ndn-traffic.log", outDirectory)
  
    TotalInterestLoss = grepData("/ndn/distributedDB/producer/host", "Total Interest Loss", "ndn-traffic.log", outDirectory)
    
    AverageRoundTripTime = grepData("/ndn/distributedDB/producer/host", "Average Round Trip Time", "ndn-traffic.log", outDirectory)

    startCountersCmd = 'cat '+outDirectory+'nfd-status-wustl-rtr_start | grep out= | cut -d{ -f4 | cut -d" " -f1 | cut -di -f1'
    finalCountersCmd = 'cat '+outDirectory+'nfd-status-wustl-rtr_final | grep out= | cut -d{ -f4 | cut -d" " -f1 | cut -di -f1'
    startCounters = subprocess.check_output(['bash','-c', startCountersCmd])
    finalCounters = subprocess.check_output(['bash','-c', finalCountersCmd])
    
    startCounters = startCounters.split('\n')
    startCounters = startCounters[:-1]
    startCounters = matrix([int(i) for i in startCounters])
    
    finalCounters = finalCounters.split('\n')
    finalCounters = finalCounters[:-1]
    finalCounters = matrix([int(i) for i in finalCounters])
    
    diff = (finalCounters - startCounters)
    totalWustl=matrix.sum(diff)
    
    multiProducersResultsDf = multiProducersResultsDf.append({'title':title, 'sent':int(clientSentInterests), 'received_orange':int(orang_serverReceivedInterests),'received_kisti':(kisti_serverReceivedInterests),'loss':float(TotalInterestLoss[:-2]),'rtt':float(AverageRoundTripTime[:-3]), 'strategy':strategy, 'dropRate':dropRate[:-1], 'total_sent_wash_u':totalWustl}, ignore_index=True)
  
  return

def plotFinals(expPrefix):
  global multiPathResultsDf
  global multiProducersResultsDf
  
  sns.set_style("white")
  sns.set_context("paper", font_scale=2.1, rc={"lines.linewidth": 2.5})
  
  if "MultipilePaths_drop" in expPrefix:
    multiPathResultsDf.strategy[multiPathResultsDf.strategy=='b2']='best-route'
    multiPathResultsDf.strategy[multiPathResultsDf.strategy=='b3']='best-route-r'
    multiPathResultsDf.strategy[multiPathResultsDf.strategy=='n']='ncc'
    multiPathResultsDf.strategy[multiPathResultsDf.strategy=='n2']='ncc-r'
    print multiPathResultsDf
    multiPathResultsDf.to_csv('/Users/user/Documents/repo/papers/forwardingStrategies/NetworkRetransmission/results/finalAnalysis/'+expPrefix+'_MergedData_multiPaths.csv')
    
    #sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 2.5})

    fig = plt.figure()
    lossPlotMultiPath = sns.barplot(x="strategy", y="loss", data=multiPathResultsDf[multiPathResultsDf.strategy=='best-route'], ci=68,palette="Blues_d")
    lossPlotMultiPath.set_ylabel('Packe loss')
    lossPlotMultiPath.set_xlabel('Stratgy')
    fig = lossPlotMultiPath.get_figure()
    fig.savefig('/Users/user/Documents/repo/papers/forwardingStrategies/NetworkRetransmission/results/finalAnalysis/'+expPrefix+'_lossPlotMultiPath.jpg')

    fig = plt.figure()
    lossPlotMultiPath_no_b2 = sns.barplot(x="strategy", y="loss", data=multiPathResultsDf[multiPathResultsDf.strategy!='best-route'],ci=68,palette="Blues_d")
    lossPlotMultiPath_no_b2.set_ylabel('Packet Rate')
    lossPlotMultiPath_no_b2.set_xlabel('Stratgy')
    fig = lossPlotMultiPath_no_b2.get_figure()
    fig.savefig('/Users/user/Documents/repo/papers/forwardingStrategies/NetworkRetransmission/results/finalAnalysis/'+expPrefix+'_lossPlotMultiPath_no_b2.jpg')

    fig = plt.figure()
    rttPlotMultiPath = sns.barplot(x="strategy", y="rtt", data=multiPathResultsDf,ci=68,palette="Blues_d")
    rttPlotMultiPath.set_ylabel('Round-Trip-Time')
    rttPlotMultiPath.set_xlabel('Stratgy')
    fig = rttPlotMultiPath.get_figure()
    fig.savefig('/Users/user/Documents/repo/papers/forwardingStrategies/NetworkRetransmission/results/finalAnalysis/'+expPrefix+'_rttPlotMultiPath.jpg')

    fig_total_sent = plt.figure()
    multi_path_total_sent = sns.barplot(x="strategy", y="total_sent_wash_u", data=multiPathResultsDf,ci=68, linewidth=0.5, palette="Blues_d")
    multi_path_total_sent.set_ylabel('Total Number of Packets Sent by WU')
    multi_path_total_sent.set_xlabel('Stratgy')
    fig_total_sent = multi_path_total_sent.get_figure()
    fig_total_sent.savefig('/Users/user/Documents/repo/papers/forwardingStrategies/NetworkRetransmission/results/finalAnalysis/'+expPrefix+'_multipath_total_sent_by_WU.jpg')

    plt.show()
  elif "MultipileProducer" in expPrefix:
    multiProducersResultsDf.dropRate[multiProducersResultsDf.dropRate=='n']='0'
    multiProducersResultsDf.strategy[multiProducersResultsDf.strategy=='b2']='best-route'
    multiProducersResultsDf.strategy[multiProducersResultsDf.strategy=='b3']='best-route-r'
    multiProducersResultsDf.strategy[multiProducersResultsDf.strategy=='n']='ncc'
    multiProducersResultsDf.strategy[multiProducersResultsDf.strategy=='n2']='ncc-r'
    print multiProducersResultsDf
    multiProducersResultsDf.to_csv('/Users/user/Documents/repo/papers/forwardingStrategies/NetworkRetransmission/results/finalAnalysis/'+expPrefix+'_MergedData_multiProducer.csv')

      #title_font = {'fontname':'Arial', 'size':'16', 'color':'black', 'weight':'normal',
      #'verticalalignment':'bottom'} # Bottom vertical alignment for more space
    axis_font = {'fontname':'Arial', 'size':'18'}


#    multi_producer_loss_no_b2 = sns.barplot(x="dropRate", y="loss", hue="strategy",data=multiProducersResultsDf[multiProducersResultsDf.strategy!='b2'], order=["n", "5","20","50"], ci=68)
#    fig_b3 = multi_producer_loss_no_b2.get_figure()
#    fig_b3.savefig('/Users/user/Documents/repo/papers/forwardingStrategies/NetworkRetransmission/results/finalAnalysis/'+expPrefix+'_multi_producer_loss_no_b2.jpg')
#    
#    multi_producer_loss = sns.barplot(x="dropRate", y="loss", hue="strategy",data=multiProducersResultsDf, order=["n", "5","20","50"], ci=68)
#    
#    fig = multi_producer_loss.get_figure()
#    fig.savefig('/Users/user/Documents/repo/papers/forwardingStrategies/NetworkRetransmission/results/finalAnalysis/'+expPrefix+'_multi_producer_loss.jpg')
#
#
    figb2 = plt.figure()
    multi_producer_loss_b2 = sns.barplot(x="dropRate", y="loss", hue="strategy",data=multiProducersResultsDf[multiProducersResultsDf.strategy=='best-route'], order=["0", "5","20","50"],ci=68, linewidth=0.5, palette="Blues_d")
    multi_producer_loss_b2.set_ylabel('Unsatasfied Interest Rate (%)')
    multi_producer_loss_b2.set_xlabel('Drop Rate (%)')
    fig_b2 = multi_producer_loss_b2.get_figure()
    fig_b2.savefig('/Users/user/Documents/repo/papers/forwardingStrategies/NetworkRetransmission/results/finalAnalysis/'+expPrefix+'_multi_producer_loss_b2.jpg')

#fig = plt.figure() # Create matplotlib figure
#    fig_b2.add_subplot(111) # Create matplotlib axes
#    multi_producer_loss_b3 = multi_producer_loss_b2.twinx()
#    width = 0.4

    fig_only_b3 = plt.figure()
    multi_producer_loss_b3 = sns.barplot(x="dropRate", y="loss", hue="strategy",data=multiProducersResultsDf[multiProducersResultsDf.strategy!='best-route'], order=["0", "5","20","50"],ci=68, linewidth=0.5, palette="Blues_d")
    
    multi_producer_loss_b3.set_ylabel('Unsatasfied Interest Rate (%)', **axis_font)
    multi_producer_loss_b3.set_xlabel('Drop Rate (%)', **axis_font)
    fig_only_b3.savefig('/Users/user/Documents/repo/papers/forwardingStrategies/NetworkRetransmission/results/finalAnalysis/'+expPrefix+'_multi_producer_loss_b3.jpg')
  
    fig_total_sent = plt.figure()
    multi_producer_total_sent = sns.barplot(x="dropRate", y="total_sent_wash_u", hue="strategy",data=multiProducersResultsDf, order=["0", "5","20","50"],ci=68, linewidth=0.5, palette="Blues_d")
    multi_producer_total_sent.set_ylabel('Total Number of Packets Sent by WU', **axis_font)
    multi_producer_total_sent.set_xlabel('Drop Rate (%)', **axis_font)
    fig_only_b3.savefig('/Users/user/Documents/repo/papers/forwardingStrategies/NetworkRetransmission/results/finalAnalysis/'+expPrefix+'_multi_producer_total_sent_by_WU.jpg')
    
#fig_fix = plt.figure() # Create matplotlib figure
    #ax = fig.add_subplot(111) # Create matplotlib axes
    #ax = multiProducersResultsDf['loss'][multiProducersResultsDf.strategy=='b2'].plot(kind="bar")
    #ax2 = multiProducersResultsDf['loss'][multiProducersResultsDf.strategy=='b3'].plot(kind="bar")
    #ax2 = ax.twinx() # Create another axes that shares the same x-axis as ax.

#width = 0.4

#   multiProducersResultsDf['loss'][multiProducersResultsDf.strategy=='b2'].plot(kind='bar', color='red', ax=ax, width=width, position=1)
#   multiProducersResultsDf['loss'][multiProducersResultsDf.strategy=='b3'].plot(kind='bar', color='blue', ax=ax2, width=width, position=0)

#   ax.set_ylabel('Unsatasfied Interest Rate')
#   ax2.set_ylabel('Unsatasfied Interest Rate')

    plt.show()
  return

if len(sys.argv) < 2:
  sys.exit("usage: python parseResults.py <expPrefix>")

expPrefix = sys.argv[1]

#expPrefix="May2_FinalRun_MultipileProducer"
rootdir ='/Users/user/Documents/repo/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/'
for subdir, dirs, files in os.walk(rootdir):
  #for file in files:
  if expPrefix in subdir:
    expName = subdir[subdir.find(expPrefix):]
    outDirectory = '/Users/user/Documents/repo/papers/forwardingStrategies/NetworkRetransmission/results/'+expName+'/'
    
    #1. copy results
    #copyDirectory(subdir, outDirectory)
    
    #2. print "plot " + expName
#plotTimeCounters(expName, outDirectory)

    #2. parse traffic data
    parseData(expName, outDirectory)


plotFinals(expPrefix)


#print multiPathResults
#df = pd.DataFrame(multiPathResults)#total = len(sys.argv)





