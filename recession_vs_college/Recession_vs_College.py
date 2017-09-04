
# coding: utf-8

# In[1]:

#Below I’ve shown how we get access to everything in the Pandas library
#– we import it! This was to note that this is the standard way to import the Pandas library.
#We should always be sure that if we are importing the entire pandas library, we follow this syntax.
#It’s common practice to use ‘pd’ as the alias. This makes it easier for others to read our code.

import pandas as pd
import numpy as np
import scipy.stats
import scipy as sp
import matplotlib.pyplot as plt
import os


# In[2]:

#reading the csv file
df = pd.read_csv('Chicago_City.csv')


# In[3]:

#In order to have a better sense of my dataset
# First five
df.head()


# In[4]:

#Last Five
df.tail()


# In[10]:

#Concise summary of a DataFrame.

df.info()


# In[6]:

#decription of the dataset.
#The percentiles to include in the output.
#Should all be in the interval [0, 1].
#By default percentiles is [.25, .5, .75],
#returning the 25th, 50th, and 75th percentiles.
df.describe()


# In[11]:

#Here I am just changing the name of index, so that it can serve me better.
df=df.rename(columns = {'Annual Salary':'salary'})
df=df.rename(columns = {'Job Titles':'Job_Titles'})


# In[12]:

#Now that I have more sense of the Dataset, and I want to compute the mean Annual Salary of the whole data.
#In order to do that, I stripped the Dollar sign($) from the salary column.
#Also, I took into account any decimal points.
#changing all to numerics

df['salary'] = df['salary'].str.replace('$', '')
df['salary'] = df['salary'].str.replace(' ', '')
df['salary'] = df['salary'].str.replace(',', '')
df['salary'] = pd.to_numeric(df['salary'], errors='coerce')


# In[13]:

#Now we can see the whole description of just salary
df['salary'].describe()


# In[15]:

#To compute the mean of the whole data set
print "Total mean of the whole Dataset: $", df['salary'].mean()


# In[17]:

#I was also interested in finding the total Mean Annual Salary of people in a certain Department.
#In this case was interested in the Department of Police.

print "Total mean of the Department of Police : $", df[df['Department'] == 'POLICE'].salary.mean()





# In[18]:

#Top 5 Job Titles with the highest Average Annual Salaries. That will be very interesting to compute.
#I sorted and grouped Job titles and Annual Salaries.

df.groupby('Job_Titles')['salary'].mean().sort_values(ascending = False)[:5]


# In[19]:

#Boxplot showing the distribution of Annual Salaries in the whole dataset

df.boxplot('salary')
plt.title('BoxPlot displaying distribution of salaries in the whole dataset')
plt.ylabel('Salary in $')
plt.show()




# In[21]:

#The “whiskers” extend to points that lie within 1.5 IQRs of the lower and upper quartile,
#then observations that fall outside this range are displayed independently. Importantly,
#this means that each value in the boxplot corresponds to an actual observation in the data:

import seaborn as sns
sns.factorplot(kind='box', y="Department", x='salary',
               data=df, size=8, aspect=1.5, legend_out=False)
plt.show()




# In[ ]:
