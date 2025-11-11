#Attempting to create predictive model maths
#VIP Weatherproof
#10/11/2025

print()
print("Attemtping to create predictive model maths")

import pandas as pd
from pandas import *
import geopandas as gpd
from scipy.stats import boxcox
import matplotlib.pyplot as plt

#IN THE FUTURE TRY AND STRUCTURE IN HEADER AND CODE FILES LIKE IN CPP

def ImportedDataFrameCode():
    #read excel spreadsheet into Pandas DataFrame
    df = pd.read_excel('/Users/ricar/Python/bolton_HV_Faults.xlsx', sheet_name=0) #https://www.geeksforgeeks.org/python/creating-a-dataframe-using-excel-files/

    #put all district names into a list
    district_names = df['District Name'].tolist() #https://www.geeksforgeeks.org/pandas/get-a-list-of-a-specified-column-of-a-pandas-dataframe/
    #remove duplicate district names by converting to a set. then back to a list to be printed (sets cannot be printed)
    district_names_2 = list(set(district_names)) #https://www.dataquest.io/blog/how-to-remove-duplicates-from-a-python-list/
    #remove bolton from the list as we want to iterate over the list to remove the locations in the list from the dataframe 
    # but we want to keep bolton in the dataframe
    district_names_2.remove("Bolton") #https://www.w3schools.com/python/python_lists_remove.asp

    #create a copy of dataframe which will be editied
    df2 = df.copy() #https://www.w3schools.com/python/pandas/ref_df_copy.asp

    #iterate over the district names in the list
    for district_name in district_names_2:
        #remove any row in the DataFrame that contains the district names in the list
        df2 = df2[df2['District Name'].str.contains(district_name) == False] #https://pandas.pydata.org/docs/reference/api/pandas.Series.str.contains.html

    #dropping all NaN/nan values from the geom_wkt column so it can be parsed to create geodataframe.
    df2=df2[df2['geom_wkt'].notna()] #https://www.geeksforgeeks.org/python/drop-rows-from-pandas-dataframe-with-missing-values-or-nan-in-columns/

    # print(district_names_3)
    # print(df2)

    #convert the incident dates and times to datetime format
    df2['Incident Date-time'] = pd.to_datetime(df2['Incident Date-time']) #https://docs.vultr.com/python/third-party/pandas/to_datetime

    df2['geom_wkt'] = df2['geom_wkt'].apply(str) #https://sparkbyexamples.com/pandas/pandas-convert-columns-to-string-type/

    #creating GeoSeries of the coordinates column from the DataFrame
    q = gpd.GeoSeries.from_wkt(df2['geom_wkt']) #https://geopandas.org/en/stable/gallery/create_geopandas_from_pandas.html

    #create GeoDataFrame from df2 to be able to handle coordinates. Had to google what the crs of the geom_wkt coordinates.
    gdf = gpd.GeoDataFrame(df2, geometry=q, crs=27700) #https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_crs.html

    #convert from crs=27700 to crs=4326 to show the coordinates in latitude and longitude.
    gdf = gdf.to_crs(4326) #https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_crs.html


    #converting lat and long to strings to flipped around as they are originally the wrong way around.
    gdf['latitude'] = gdf['geometry'].y
    gdf['longitude'] = gdf['geometry'].x
    #concatenating strings the correct way round.
    gdf['coordinates'] = gdf['geometry'].y.apply(str) + " " + gdf['geometry'].x.apply(str)


    #gdf['geometry'] = gdf.apply(lambda row: Point(row['y'], row['x']), axis=1)

    # print(df2['Incident Date-time'])
    #getting all direct causes into a list
    coordinates = gdf['coordinates'].tolist() 
    coordinates = list(set(coordinates))

    #writing coordinates into a text file.
    with open('coordinates.txt', 'w+') as f: #https://www.geeksforgeeks.org/python/reading-and-writing-lists-to-a-file-in-python/
        
        # write elements of list
        for items in coordinates:
            f.write('%s\n' %items)
    f.close()

    #creating a dictionary to hold dataframes sorted by coordinate location
    df_dict = {}

    #creating a new dataframe for each coordinate
    for i in coordinates:
        df_dict[i] = pd.DataFrame()
        
    #iterating through the coordinates. if a row of df2 has the coordinates of the current coordinate iteration it will be put into the dataframe.
    for coordinate in coordinates:
        df_dict[coordinate] = gdf[gdf['coordinates']==coordinate] 
        
    return df2    

def commentBlock():
    '''
    I'm thinking of many ways to predict the outcome of the analysis as well as how to make it more efficient
    First, to make the coordinates easier to use we could pool the coorinates into bigger boxes. 
    I actually have two ideas for this
    The better one is actually to treat the coordinates like a big matrix and use a pooling layer to apprioximate
    the most relevant data from entire days in bigger areas
    Think of it like this,
    let's assign every cause a value - In this case I'm going to use the 'Direct cause category' since there are less of them
    we have four grid locations : [ 1,2    1,3 ]  with four identifiers [ 1    1 ] where 1 is companies and 2 is 
                                  [ 2,2    2,3 ]                        [ 2    1 ]
    weather. The idea is this, before our program does the time series analysis it pools together grid data, first day by day,
    and second by cause. https://www.geeksforgeeks.org/deep-learning/cnn-introduction-to-pooling-layer
    Then, we can cut down on how long it takes to process the 50 hours.
    Naturally, in the final deliverable the computer's prediction would be based on the larger area as opposed to the smaller one   
    
    In all honesty, I;ve been thinking about this for about a week, you could totally neural network this. I thinkn it's
    probably too much, but it could be a good idea for a predictive model in the future
    '''
    
def boxCox():
    '''
    boxCoxData = Series(boxcox(), index = )
    plt.grid()
    plt.plot(boxCoxData, label='After Box Cox tranformation')
    boxCoxDataDiff = Series(boxCoxData - boxCoxData.shift(), )
    plt.plot(boxCoxDataDiff, label='After Box Cox tranformation and differencing')
    plt.legend(loc='best')
    plt.title('After Box Cox transform and differencing')
    plt.show()
    
    boxCoxDataDiff.dropna(inplace=True)
    boxCoxDataDiff.tail()
    
    return boxCoxDataDiff, boxCoxData
    '''
    
df2 = ImportedDataFrameCode()

causes = df2['Direct Cause Category'].tolist() 
causes = list(set(causes))



