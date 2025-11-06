#this is the main file
import pandas as pd
import geopandas as gpd

#read excel spreadsheet into Pandas DataFrame
df = pd.read_excel('/Users/razin/Documents/enwl_fault_data copy.xlsx', sheet_name=2) #https://www.geeksforgeeks.org/python/creating-a-dataframe-using-excel-files/

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
    
#variable to hold max size of dataframe
max_size = 0
#variable to hold coordinate with most outages/faults.
point = ''
#creating dataframe to hold data for the coordinate with the most outages/faults
point_df = pd.DataFrame()
    
#iterating through the dictionary
for dfi in df_dict:
    #checking for the coordinate dataframe with the most outages.
    if len(df_dict[dfi]) > max_size:
        max_size = len(df_dict[dfi])
        
for dfx in df_dict:
    #looking for the dataframe with the new found max size
    if len(df_dict[dfx]) == max_size:
        point = dfx
        point_df = df_dict[dfx]
        print(point)
        print(point_df)