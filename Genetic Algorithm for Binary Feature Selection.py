# -*- coding: utf-8 -*-
"""GA Naive Bayes Classifier- Hrishikesh (Shared).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1urbJrcidgqt12LiU4ryqKR_SWjO-od_1
"""

CR=0.8 #Cross-over rate
MR=0.01 #Mutation rate

import pandas as pd
import numpy as np

data=pd.read_csv('ionosphere.csv') #Load the dataset
data.head()

data.shape

rows, columns= data.shape[0], data.shape[1]

NP=10 #Number of population
D=columns-1 #Size of the problem

#Separate the features and output column

y=data.iloc[:,-1]
tdata=data.iloc[:,0:-1]
tdata.head()

from sklearn.model_selection import train_test_split

training_data,testing_data,training_classlebel,testing_classlebel=train_test_split(tdata,y,test_size=0.2,random_state=42)
training_data.shape,testing_data.shape,training_classlebel.shape,testing_classlebel.shape

import random

#Naive Bayes Classifier is used in this problem

from sklearn.naive_bayes import GaussianNB

nb = GaussianNB()

from numpy.core.fromnumeric import cumsum

X=np.zeros((NP,D),dtype=int)
fit=np.zeros((NP))

for i in range(NP):
  for d in range(D):
    if random.random()>0.5:
      X[i,d]=1

X

#Calculating fitness for each individual

for i in range(NP):
  if((training_data.iloc[:,X[i,:]==1]).shape[1]==0):
    fit[i]=0.5
  else:
    o1=nb.fit(training_data.iloc[:,X[i,:]==1],training_classlebel)
    Ac1=o1.predict(testing_data.iloc[:,X[i,:]==1])
    fit[i]=sum(Ac1!=testing_classlebel)/testing_data.shape[0]

t=1
curve=[] #List to store fitness
while t<=200:
  #convert error to accuracy (inverse of fitness)
  Ifit=1-fit
  Prob=Ifit/sum(Ifit) #Fitness Probability is calculated

  #Crossover
  X1=[]
  X2=[]

  for i in range(NP):
    if random.random()<CR:
      #Cumulative Summation
      C=cumsum(Prob)
      #Random one value, most probability value [0-1]
      P=random.random()
      #Route wheel
      for j in range(len(C)):
        if C[j]>P:
          Route=j
          break
      k1=Route
      k2=Route

      #Store parents
      P1=X[k1,:]
      P2=X[k2,:]

      #Random select one crossover point
      ind=random.randint(0,D-1)

      #Single point crossover between two parents
      X1.append((np.append(P1[0:ind],P2[ind:D])).tolist()) #Each newly generated offspring is getting added to X1 and X2
      X2.append((np.append(P2[0:ind],P1[ind:D])).tolist())

  #Union
  Xnew=X1+X2
  Nc=len(Xnew)
  Fnew=np.zeros(Nc) #Generate a fitness array for the new generation individuals
  Xnew=np.array(Xnew) #Convert the list Xnew to 2-D array

  #Mutation
  for i in range(Nc):
    for d in range(D):
      if random.random()<=MR:
        #Mutate from 0 to 1 or from 1 to 0
        Xnew[i,d]=1-Xnew[i,d]

    #Fitness
    if((training_data.iloc[:,Xnew[i,:]==1]).shape[1]==0):
      Fnew[i]=0.5
    else:
      o1=nb.fit(training_data.iloc[:,Xnew[i,:]==1],training_classlebel)
      Ac1=nb.predict(testing_data.iloc[:,Xnew[i,:]==1])
      Fnew[i]=sum(Ac1!=testing_classlebel)/testing_data.shape[0]

  #Merge Population
  XX=np.concatenate((X,Xnew),axis=0) #We merge the population of the previous generation and the new generation
  FF=np.append(fit,Fnew) #We merge the fitness of the previous generation and the new generation
  # print(FF)

  #Select N best solution
  idx=np.argsort(FF) #Returns an array of indices that would sort the array
  FF=np.sort(FF)
  X=XX[idx[0:NP],:] #Select 10 best rows according to the sorted indices
  fit=FF[0:NP]

  #Best Chromosomes
  Xgb=X[0,:]
  fitG=fit[0]
  curve.append(fitG)
  #print(XX)

  t=t+1

#Select features based on selected index

Sf=[] #Position of the columns that are going to be passed

for k in range(D):
  if Xgb[k]==1:
    Sf.append(k)

Nf=len(Sf)

print("Selected feature indices are: ",Sf)
print("Number of selected features are: ",Nf)

#Accuracy without FS

o1=nb.fit(training_data,training_classlebel)
Ac1=nb.predict(testing_data)
Fnew1=sum(Ac1==testing_classlebel)/testing_data.shape[0]*100
print("Accuracy without FS: ", Fnew1)

#Accuracy with FS

o1=nb.fit(training_data.iloc[:,Sf],training_classlebel)
Ac1=nb.predict(testing_data.iloc[:,Sf])
Fnew2=sum(Ac1==testing_classlebel)/testing_data.shape[0]*100
print("Accuracy with FS: ",Fnew2)

import matplotlib.pyplot as plt

fig=plt.figure()
ax=fig.add_subplot()
fig.show()

ax.plot(curve, color='r')
fig.canvas.draw()