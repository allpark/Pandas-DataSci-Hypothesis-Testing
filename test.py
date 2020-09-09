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

    # return uni town mainframe indexed by a number
    return uni_towns

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel("data/gdplev.xls", skiprows=8, header=None, 
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
    
    gdp = pd.read_excel("data/gdplev.xls", skiprows=8, header=None, 
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

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''

    
    gdp = pd.read_excel("data/gdplev.xls", skiprows=8, header=None, 
                        usecols = [4,5,6]
    )
    gdp.columns = ["Quarter","GDP Billions", "GDP Billions Chained"]
    
    
    recession_start_quarter = get_recession_start()
    recession_end_quarter   = get_recession_end()
    
    recession_start_year = int(recession_start_quarter[:4])
    recession_end_year   = int(recession_end_quarter[:4])
    
    # select gdp entries from start to end of recession
    temp = gdp["Quarter"].str.slice(stop=-2).astype("int")
    gdp = gdp[ (temp >= recession_start_year) & (temp <= recession_end_year)]

    bottom_quarter = None
    bottom_gdp     = None
    
    for i in range(0,len(gdp)):
        
        frame = gdp.iloc[i]
        
        if (frame["Quarter"]==recession_start_quarter):
            bottom_quarter, bottom_gdp = frame["Quarter"], frame["GDP Billions Chained"]
        else:
            if (bottom_quarter):
                if (frame["GDP Billions Chained"] < bottom_gdp) and frame["Quarter"] != recession_end_quarter:  
                    bottom_quarter, bottom_gdp = frame["Quarter"], frame["GDP Billions Chained"]

    return bottom_quarter

# helper function for grouping year-month into year-quarter 
def convert_to_quarter(year_month):
    y, mo = year_month.split("-")
    if mo in ["01","02","03"]:
        result = y + 'q1'
    elif mo in ["04","05","06"]:
        result = y + 'q2'
    elif mo in ["07","08","09"]:
        result = y + 'q3'
    else:
        result = y + 'q4'
    return result
    
def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    housing_data = pd.read_csv("data/City_Zhvi_AllHomes.csv")
    
    cols_to_keep = ["RegionID", "RegionName", "State"]
    
    # get years columns 
    for year in range(2000,2017):
        for column in housing_data.columns:
            if column.startswith(str(year)):
                cols_to_keep += [column]
    
    housing_data = housing_data[cols_to_keep]
    housing_data["State"] = housing_data["State"].replace(states)
    
    # Stack the columns of GDP values and add a quarter column
    result = housing_data.copy()
    result = result.set_index(["State", "RegionName", "RegionID"]).stack(dropna=False)
    
    result = result.reset_index().rename(columns={"level_3": "YearMonth", 0: "GDP"}).drop_duplicates()

    # convert year month elements into quarters 
    result["Quarter"] = result["YearMonth"].apply(convert_to_quarter)
    result = result.drop("YearMonth", axis=1)

    # create pivot table 
    out = result.pivot_table(
        values="GDP",
        index=["State", "RegionName", "RegionID"],
        columns="Quarter", 
        aggfunc=np.mean
    )
    
    out = out.reset_index().drop('RegionID', axis=1)

    return out.set_index(['State', 'RegionName'])

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    # get university towns
    uni_towns = get_university_town_names()
    uni_towns["uni_town"] = 1
    uni_towns = uni_towns.set_index(["State", "RegionName"])

    # get housing data and merge with housing prices by state and region name
    housing_data = convert_housing_data_to_quarters()
    
    housing_data = housing_data.merge(
        uni_towns, 
        how="left", 
        left_index=True,
        right_index=True
    )
    
    # set null uni_town to false 
    housing_data.uni_town[housing_data.uni_town.isnull()] = 0

    # start analyzing trends 
    recession_start  = get_recession_start()
    recession_bottom = get_recession_bottom()
      
    selected = housing_data[[recession_start, recession_bottom,"uni_town"]]
    selected["Delta"] = selected[recession_bottom] / selected[recession_start]
    
    uni_towns     = selected[selected["uni_town"]==1]["Delta"].dropna()
    not_uni_towns = selected[selected["uni_town"]==0]["Delta"].dropna()

    test = ttest_ind(uni_towns, not_uni_towns, nan_policy="omit")
    
    # get p value
    p = test[1]
    
    # find if they're different or not by comparing with alpha value 
    diff = None
    if p < 0.01:
        diff = True
    else:
        diff = False
    
    better = ""
    if uni_towns.mean() < not_uni_towns.mean():
        better = "non-university town"
    else:
        better = "university town"
    
    return (diff, p, better)

run_ttest()
       
  
