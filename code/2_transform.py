import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here

#Reading in data sets
surveys = pd.read_csv('cache/survey.csv')

states = pd.read_csv('cache/states.csv')

#Getting unique years of surveys
years = surveys['year'].unique()

#Creating an empty list to store COL dfs in
cols = []

#For each year, loading its COL data set and storing it in list
for year in years:
    col = pd.read_csv(f'cache/col_{year}.csv')
    cols.append(col)

#Combining all dataframes in the list
col_data = pd.concat(cols, ignore_index = False)

#Creating a new column with cleaned USA values
surveys['_country'] = surveys['What country do you work in?'].apply(pl.clean_country_usa)

#Merging surveys and states dfs to get state codes associated with surveys
survey_states_combined = pd.merge(left = surveys, right = states, how = 'inner', left_on = "If you're in the U.S., what state do you work in?", right_on = "State")

#Combining city name, state code, and country into new column
survey_states_combined['_full_city'] = survey_states_combined["If you're in the U.S., what state do you work in?"] + ', ' + survey_states_combined['Abbreviation'] + ', ' + survey_states_combined['_country']

#merging the surveys dataset with the COL by city data set
combined = pd.merge(survey_states_combined, col_data, how = 'inner', left_on = ['year', '_full_city'], right_on = ['year', 'City'])

#Cleaning the salary column for further processing
combined['__annual_salary_cleaned'] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency)

#Standardizing annual salary based on COL
combined['_annual_salary_adjusted'] = combined.apply(lambda row: (100/row['Cost of Living Index']) * row['__annual_salary_cleaned'], axis = 1)

#Outputing combined df to a CSV file
combined.to_csv('cache/survey_dataset.csv')

#Creating a pivot table of cities, ages, and the means of average salaries
annual_salary_adjusted_by_location_and_age = combined.pivot_table(index = '_full_city', columns = 'How old are you?', values = '_annual_salary_adjusted', aggfunc = 'mean')

#Exporting previous pivot table as CSV
annual_salary_adjusted_by_location_and_age.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')

#Creating pivot table of cities, education, and means of average salaries
annual_salary_adjusted_by_location_and_education = combined.pivot_table(index = '_full_city', columns = 'What is your highest level of education completed?', values = '_annual_salary_adjusted', aggfunc = 'mean')

#Exporting previous pivot table to CSV
annual_salary_adjusted_by_location_and_education.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')

