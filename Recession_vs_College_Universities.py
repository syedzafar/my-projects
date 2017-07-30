
# coding: utf-8

# In[94]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import matplotlib
import numpy 
import pandas
import statsmodels.stats.api as statsmodels
from pylab import rcParams


# In[93]:


states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[ ]:





# In[87]:


'''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    


def get_list_of_university_towns():
        university_towns = open('university_towns.txt').readlines()
        university_towns = [x.split('(')[0] for x in university_towns]
        df_uni_town = []
        for name in university_towns:
            if '[edit]' in name:
                statename = name.split('[edit]')[0]
            else:
                df_uni_town.append({'State':statename, 'RegionName':name})
        df = pd.DataFrame(df_uni_town,columns =['State','RegionName'])
        return df
get_list_of_university_towns()
    


# In[88]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    gdplev = pd.ExcelFile('gdplev.xls')
    gdplev = gdplev.parse("Sheet1", skiprows=219)
    gdplev = gdplev[['1999q4', 9926.1]]
    gdplev.columns = ['Quarter','GDP']
    for num in range(2, len(gdplev)):
        if (gdplev.iloc[num-2][1] > gdplev.iloc[num-1][1]) and (gdplev.iloc[num-1][1] > gdplev.iloc[num][1]):
            return gdplev.iloc[num-2][0]
get_recession_start()


# In[89]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    gdplev = pd.ExcelFile('gdplev.xls')
    
    gdplev = gdplev.parse("Sheet1", skiprows=219)
    
    gdplev = gdplev[['1999q4', 9926.1]]
    
    gdplev.columns = ['Quarter','GDP']
    start = get_recession_start()
    
    start_index = gdplev[gdplev['Quarter'] == start].index.tolist()[0]
    
    gdplev=gdplev.iloc[start_index:]
    
    for i in range(2, len(gdplev)):
        if (gdplev.iloc[i-2][1] < gdplev.iloc[i-1][1]) and (gdplev.iloc[i-1][1] < gdplev.iloc[i][1]):
            return gdplev.iloc[i][0]
get_recession_end()


# In[73]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    gdplev = pd.ExcelFile('gdplev.xls')
    
    gdplev = gdplev.parse("Sheet1", skiprows=219)
    
    gdplev = gdplev[['1999q4', 9926.1]]
    
    gdplev.columns = ['Quarter','GDP']
    
    start = get_recession_start()
    
    start_index = gdplev[gdplev['Quarter'] == start].index.tolist()[0]

    end = get_recession_end()
   
    end_index = gdplev[gdplev['Quarter'] == end].index.tolist()[0]
    
    gdplev=gdplev.iloc[start_index:end_index+1]
    
    bottom = gdplev['GDP'].min()
    
    bottom_index = gdplev[gdplev['GDP'] == bottom].index.tolist()[0]-start_index
    
    return gdplev.iloc[bottom_index]['Quarter']
get_recession_bottom()


# In[90]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    houses = pd.read_csv('City_Zhvi_AllHomes.csv')
    for i in range(2000,2017):
        if i == 2016:
            houses[str(i) + 'q1'] = houses[[str(i)+'-01', str(i)+'-02', str(i)+'-03']].mean(axis=1)
            houses[str(i) + 'q2'] = houses[[str(i)+'-04', str(i)+'-05', str(i)+'-06']].mean(axis=1)
            houses[str(i) + 'q3'] = houses[[str(i)+'-07', str(i)+'-08']].mean(axis=1)
        else:
            houses[str(i) + 'q1'] = houses[[str(i)+'-01', str(i)+'-02', str(i)+'-03']].mean(axis=1)
            houses[str(i) + 'q2'] = houses[[str(i)+'-04', str(i)+'-05', str(i)+'-06']].mean(axis=1)
            houses[str(i) + 'q3'] = houses[[str(i)+'-07', str(i)+'-08', str(i)+'-09']].mean(axis=1)
            houses[str(i) + 'q4'] = houses[[str(i)+'-10', str(i)+'-11', str(i)+'-12']].mean(axis=1)

    houses = houses.drop(houses.columns[[0] + list(range(3,251))],axis=1)
    houses = houses.replace({'State':states})
    houses = houses.set_index(['State', 'RegionName'])
    return houses

convert_housing_data_to_quarters()



# In[92]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) 
    where 
    
    different=True if the t-test is True at a p<0.01 (we reject the null hypothesis), 
    different=False if otherwise (we cannot reject the null hypothesis). 
    
    The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    data = convert_housing_data_to_quarters().copy()
    print data
    data = data.loc[:,'2008q3':'2009q2']
    data = data.reset_index()
    def price_ratio(row):
        return (row['2008q3'] - row['2009q2'])/row['2008q3']
    
    data['up&down'] = data.apply(price_ratio,axis=1)
    #uni data 
    
    uni_town = get_list_of_university_towns()['RegionName']
    uni_town = set(uni_town)

    def is_uni_town(row):
        #check if the town is a university towns or not.
        if row['RegionName'] in uni_town:
            return 1
        else:
            return 0
    data['is_uni'] = data.apply(is_uni_town,axis=1)
    
    
    not_uni = data[data['is_uni']==0].loc[:,'up&down'].dropna()
    is_uni  = data[data['is_uni']==1].loc[:,'up&down'].dropna()
    def better():
        if not_uni.mean() < is_uni.mean():
            return 'non-university town'
        else:
            return 'university town'
    p_val = list(ttest_ind(not_uni, is_uni))[1]
    result = (True,p_val,better())
    return result
run_ttest()


# In[ ]:


Conclusion
The result of our t-test shows us that we can confidently say that college towns were more resilient against the "Great Recession" starting in 2008. Our p-value fell well below the .01 threshold. This means that whether a city was a college town or not played a significant role in the change of its mean house price in the time spanning the start of the recession to the bottom of the recession.

