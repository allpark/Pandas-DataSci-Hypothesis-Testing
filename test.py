import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Hypothesis Testing Using Numpy and Pandas

#Definitions:

#     * A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
#     * A recession is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
#     * A university town is a city which has a high percentage of university students compared to the total population of the city.

# Hypothesis

# University towns have their mean housing prices less effected by recessions.
# Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. 

# create a dictionary for converting short-hand state names to full name 
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def get_university_town_names():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:
    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    # create data frame to store state and region names of university towns 
    uni_towns = pd.DataFrame(columns=["State", "RegionName"])
    
    # open text file, read towns and clean data
    with open("data/university_towns.txt") as f:
        
        # create current state variable to keep track of which
        # state entries we are looking at 
        current_state = None
        
        # create indexing variable to keep track of how many entries we have so far
        index = 0
        
        # go through every town in file
        for town in f:
            
            # remove trailing characters from town names
            name = town.rstrip()
            
            # if we've discovered a new state, set current state to the state and remove "[edit]" from it 
            if name[-6:]=="[edit]":
                current_state = name[:-6]
            else:
            
                
                # segment region, retrieve name before parenthesis, and remove whitespace
                region = name.split("(")[0].strip()
    
                # append to data frame
                uni_towns = uni_towns.append(
                    
                    pd.DataFrame(
                        {
                            "State" :  current_state,                            
                            "RegionName" : region
                        },
                        
                        index = [index],
                        

                    ),

                    # disable sorting 
                    sort=False
                
                )
              
                # increment index by 1 
                index += 1


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel("gdplev.xls", skiprows=8, header=None, 
                        usecols = [4,5,6]
    )
    gdp.columns = ["Quarter","GDP Billions", "GDP Billions Chained"]
    
    # start year for mask clipping
    start_from = 2000
    
    # create mask by stripping q1-4 from years and then performing bool operations 
    mask = gdp["Quarter"].str.slice(stop=-2).astype("int")>=start_from
    
    # clip data frame given mask
    gdp  = gdp[mask]
    
    # start linearly searching for two consecutive negative drops in gdp where ... xn > xn+1 > xn+2  

    # from the first index to the (last element-3) as we're going to be looking up three elements in one pass
    for i in range(0, len(gdp.index)-2):
        
        frame0, frame1, frame2 = gdp.iloc[i], gdp.iloc[i+1], gdp.iloc[i+2]
        
        # use the second frame quarter as it marks the beginning of a recession
        quarter_start = frame1["Quarter"]
        
        # condition must satisfy : xn > xn+1 > xn+2  
        in_recession    = frame0["GDP Billions Chained"] > frame1["GDP Billions Chained"] > frame2["GDP Billions Chained"]
        
        if (in_recession):
            return quarter_start
        
    return False


def get_recession_end():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel("gdplev.xls", skiprows=8, header=None, 
                        usecols = [4,5,6]
    )
    gdp.columns = ["Quarter","GDP Billions", "GDP Billions Chained"]
    
    # get depression start year
    start_from = int(get_recession_start()[:4])
   
    # create mask by stripping q1-4 from years and then performing bool operations 
    mask = gdp["Quarter"].str.slice(stop=-2).astype("int")>=start_from
    
    # clip data frame given mask
    gdp  = gdp[mask]

    # from the first index to the (last element-3) as we're going to be looking up three elements in one pass
    for i in range(0, len(gdp.index)-2):
        
        frame0, frame1, frame2 = gdp.iloc[i], gdp.iloc[i+1], gdp.iloc[i+2]
        
        # use the second frame quarter as it marks the beginning of a recession
        quarter_end = frame2["Quarter"]
        
        # condition must satisfy : xn > xn+1 > xn+2  
        out_recession    = frame0["GDP Billions Chained"] < frame1["GDP Billions Chained"] < frame2["GDP Billions Chained"]
        
        if (out_recession):
            return quarter_end
        
    return False


       
  
