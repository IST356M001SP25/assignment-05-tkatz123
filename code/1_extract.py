import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
  
#TODO Write your extraction code here


#Extracts the states csv
states = pd.read_csv('https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv')

#Ensures csv was imported correctly
print(states.head())

#Saves csv to cache folder
states.to_csv('cache/states.csv', index = False)


#Extracts survey csv
surveys = pd.read_csv('https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv')

#Verifies csv was imported correctly
print(surveys.head())

#Extracts the year from timestamps and stores it in new column
surveys['year'] = surveys['Timestamp'].apply(pl.extract_year_mdy)

#Verifies head column created correctly
print(surveys['year'].head())

surveys.to_csv('cache/survey.csv', index = False)

#Gets each unique year for the surveys
unique_years = surveys['year'].unique()


for year in unique_years:
    #Extracts quallity of living info
    col = pd.read_html(f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0")
    col = col[1]

    #Extracts rows matching year searched for
    col['year'] = year

    #Exports each df to csv
    col.to_csv(f'cache/col_{year}.csv', index = False)
