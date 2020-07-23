import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

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
    with open("university_towns.txt") as f:
        
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
                        
                        index = [index]

                    ),
                
                )
              
                # increment index by 1 
                index += 1
  
# to do: complete get recession function
def getRecession(year):
  
