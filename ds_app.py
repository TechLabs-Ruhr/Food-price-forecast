import streamlit as st
import numpy as np
import pandas as pd
import eurostat
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline


st.title("Food Price Analysis")

#Define a dictionary mapping country names to their abbreviations
country_abbr = { 'Austria' : 'AT',
                 'Belgium' : 'BE',
                 'Bulgaria' : 'BG',
                 'Croatia' : 'HR',
                 'Denmark' : 'DK',
                 'Estonia' : 'ES',
                 'Finland' : 'FI',
                 'France' : 'FR',
                 'Germany' : 'DE',
                 'Greece' : 'EL',
                 'Hungary' : 'HU',
                 'Ireland' : 'IE',
                 'Italy' : 'IT',
                 'Latvia' : 'LV',
                 'Lithuania' : 'LT',
                 'Luxembourg' : 'LU',
                 'Malta' : 'MT',
                 'Netherlands' : 'NL',
                 'Norway' : 'NO',
                 'Poland' : 'PL',
                 'Portugal' : 'PT',
                 'Romania' : 'RO',
                 'Slovakia' : 'SK',
                 'Slovenia' : 'SI',
                 'Spain' : 'ES',
                 'Sweden' : 'SE',
                 'Türkiye' : 'TR'}

# Define a dictionary mapping food categories to their abbreviations
food_abbr = { 'Food' : 'CP011',
              'Bread': 'CP01113',
              'Meat' : 'CP0112',
              'Fish and seafood' : 'CP0113',
              'Milk, cheese and eggs' : 'CP0114',
              'Fruit' : 'CP0116',
              'Vegetables' : 'CP0117',
              'Potatoes' : 'CP01174',
              'Beer' : 'CP0213'}

# Sidebar for country selection
eu_countries = list(country_abbr.keys())
eu_selection = st.sidebar.selectbox("Select a country:", eu_countries)
eu_abbr = country_abbr.get(eu_selection) # Get the abbreviation corresponding to the selected country.

# Food category selection sidebar
food_prices = list(food_abbr.keys())
food_selection = st.sidebar.selectbox("Select a food category:", food_prices)
fp_abbr = food_abbr.get(food_selection) # Get the abbreviation corresponding to the selected food category.



# Food Price
# Define the code for the Eurostat dataset
code_fp = 'PRC_HICP_MIDX'

# Define a filter to select specific data and retrieve the data from Eurostat based on the code and filter parameters
my_filter_pars_fp = {'startPeriod' : 1996, 'geo' : [eu_abbr], 'coicop' : [fp_abbr], 'unit' : 'I15'}
fp = eurostat.get_data_df(code_fp, filter_pars = my_filter_pars_fp)

# Adjustment of the data frame
fp = fp.drop(['freq', 'unit', 'coicop', 'geo\TIME_PERIOD'], axis=1) # Drop columns
fp = fp.melt(var_name='Date', value_name= fp_abbr) # Reshape the DataFrame by melting it to have a 'Date' column and a 'Food Price (€)' column

# Check and replace column names
fp.columns.name = None  # Clear the column names' name attribute

# Iterate through the columns and replace names based on a dictionary
for col in fp.columns:
    if col in food_abbr.values():
        key = [k for k, v in food_abbr.items() if v == col][0]
        new_col_name_fp = key + ' Price (€)'
        fp.rename(columns={col: new_col_name_fp}, inplace=True)



#Eltricity price
# Define the code for the Eurostat dataset
code_ep = 'NRG_PC_205'

# Define a filter to select specific data and retrieve the data from Eurostat based on the code and filter parameters
my_filter_pars_ep = {'startPeriod' : 2007, 'geo' : [eu_abbr], 'tax' : 'X_TAX', 'nrg_cons' : ['MWH_LT20', 'MWH20-499', 
                                                                    'MWH500-1999', 'MWH2000-19999', 
                                                                    'MWH20000-69999', 'MWH70000-149999', 
                                                                    'MWH_GE150000' ], 'currency' : 'EUR' }
ep = eurostat.get_data_df(code_ep, filter_pars = my_filter_pars_ep)

# Adjustment of the data frame
ep = ep.drop(['freq', 'product', 'unit', 'tax', 'currency', 'nrg_cons', 'geo\TIME_PERIOD'], axis=1) # Drop columns
average = ep.mean(skipna=True).to_frame().T # Calculate the average over each column and ignore NaN values
ep = pd.concat([ep, average], axis=0) # Append the average row to the DataFrame
ep = ep.reset_index()
ep = ep.drop('index', axis=1)
ep = ep.drop(index=range(7)) # Drop all rows except for the average row
ep = ep.reset_index()
ep = ep.drop('index', axis=1)
ep = ep.melt(var_name='Date', value_name='€/kWh') # Reshape the DataFrame by melting it to have a 'Date' column and a '€/kWh' column

# Extend the data by repeating each row in the DataFrame 6 times
ep = ep.loc[np.repeat(ep.index, 6)].reset_index(drop=True)

# Define the list of time values
time_values = [
    '2007-01', '2007-02', '2007-03', '2007-04', '2007-05', '2007-06', '2007-07', '2007-08', '2007-09', '2007-10',
    '2007-11', '2007-12', '2008-01', '2008-02', '2008-03', '2008-04', '2008-05', '2008-06', '2008-07', '2008-08',
    '2008-09', '2008-10', '2008-11', '2008-12', '2009-01', '2009-02', '2009-03', '2009-04', '2009-05', '2009-06',
    '2009-07', '2009-08', '2009-09', '2009-10', '2009-11', '2009-12', '2010-01', '2010-02', '2010-03', '2010-04',
    '2010-05', '2010-06', '2010-07', '2010-08', '2010-09', '2010-10', '2010-11', '2010-12', '2011-01', '2011-02',
    '2011-03', '2011-04', '2011-05', '2011-06', '2011-07', '2011-08', '2011-09', '2011-10', '2011-11', '2011-12',
    '2012-01', '2012-02', '2012-03', '2012-04', '2012-05', '2012-06', '2012-07', '2012-08', '2012-09', '2012-10',
    '2012-11', '2012-12', '2013-01', '2013-02', '2013-03', '2013-04', '2013-05', '2013-06', '2013-07', '2013-08',
    '2013-09', '2013-10', '2013-11', '2013-12', '2014-01', '2014-02', '2014-03', '2014-04', '2014-05', '2014-06',
    '2014-07', '2014-08', '2014-09', '2014-10', '2014-11', '2014-12', '2015-01', '2015-02', '2015-03', '2015-04',
    '2015-05', '2015-06', '2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12', '2016-01', '2016-02',
    '2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09', '2016-10', '2016-11', '2016-12',
    '2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', '2017-08', '2017-09', '2017-10',
    '2017-11', '2017-12', '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08',
    '2018-09', '2018-10', '2018-11', '2018-12', '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06',
    '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12', '2020-01', '2020-02', '2020-03', '2020-04',
    '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12', '2021-01', '2021-02',
    '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09', '2021-10', '2021-11', '2021-12',
    '2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06', '2022-07', '2022-08', '2022-09', '2022-10',
    '2022-11', '2022-12']

ti = pd.DataFrame({'Time':time_values}) # Create a DataFrame 'ti' with the 'Time' column containing time_values
ep1 = ep.merge(ti, left_on='Date', right_on='Time') # Merge the 'ep' DataFrame with the 'ti' DataFrame using the 'Date' and 'Time' columns

# Fill missing values in the 'Time' and '€/kWh' columns using corresponding values from 'ti' and 'ep'
ep1['Time'] = ti['Time'].fillna(ep1['Time'])
ep1['€/kWh'] = ep['€/kWh'].fillna(ep1['€/kWh'])

# Adjustment of the data frame
ep = ep1.drop('Date', axis=1)
ep.rename(columns={'Time': 'Date'}, inplace=True)
new_columns_order = ['Date', '€/kWh']
ep = ep[new_columns_order]


# Exchange Rate
# Define the code for the Eurostat dataset
code_exp = 'ERT_BIL_EUR_M'

# Define a filter to select specific data and retrieve the data from Eurostat based on the code and filter parameters
my_filter_pars_exp = {'startPeriod' : 1996, 'currency' : 'USD', 'statinfo' : 'AVG'}
exp = eurostat.get_data_df(code_exp, filter_pars = my_filter_pars_exp)

# Adjustment of the data frame
exp = exp.drop(['freq','statinfo','unit','currency\TIME_PERIOD'], axis=1) # Drop columns
exp = exp.melt(var_name='Date', value_name='Exchange Rate ($/€)') # Reshape the DataFrame by melting it to have a 'Date' column and a 'Food Price (€)' column



# Brent Oil Price
# Read the data
bop = pd.read_csv('Datasets/Oil_price/Brent.csv', sep=";", header=0)

# Adjustment of the data frame
bop = bop.drop(bop.columns[2:7], axis=1) # Drop columns
bop.rename(columns={'Datum': 'Date'}, inplace=True) # Change the Name
bop.rename(columns={'Zuletzt': 'Oil Price (USD per gallon)'}, inplace=True) # Change the Name

# Apply a lambda function to replace ',' with '.' in all columns of the DataFrame 'bop'
bop = bop.apply(lambda x: x.str.replace(',','.'))
bop['Oil Price (USD per gallon)'] = bop['Oil Price (USD per gallon)'].astype(float) # Change dtype



# Weather Data (only Germany)
# List of month names
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Loading the data 
temp_data = []
pre_data = []

# Loop through the list of month names
for month_name in months:
    temp_filename = f'Datasets/Weather_data/Temperature/{month_name}.txt' # source: https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/monthly/air_temperature_mean/
    pre_filename = f'Datasets/Weather_data/Precipitation/{month_name}.txt' # source: https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/monthly/precipitation/
    
    try:
        # Attempt to read the temperature and precipitation data from the respective files
        temp_df = pd.read_csv(temp_filename, sep=";", header=1)
        pre_df = pd.read_csv(pre_filename, sep=";", header=1)
        
        # Append the loaded dataframes to the respective lists
        temp_data.append(temp_df)
        pre_data.append(pre_df)
        
    except FileNotFoundError:
        # If the file for a specific month is not found, print a message
        print(f'File for {month_name} not found.')

# This class removes data rows where the year is less than 1996
class DataDropper(BaseEstimator, TransformerMixin):
    def __init__(self, min_year=1996):
        self.min_year = min_year

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[X["Jahr"] >= self.min_year].reset_index(drop=True)
    
    
# This class creates a new column "Date" by combining year and month 
class ColumnCreater(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Check if the "Date" column already exists, otherwise create it
        if "Date" not in X.columns:
            X["Date"] = ""
        # Loop through the rows of the DataFrame to create the "Date" column
        for index, row in X.iterrows():
            if row["Monat"] < 10:
                X.at[index, "Date"] = str(row["Jahr"]) + "-0" + str(row["Monat"])
            else:
                X.at[index, "Date"] = str(row["Jahr"]) + "-" + str(row["Monat"])    
        return X
  

# This class changes the column name "Germany"   
class ColumnRenamer(BaseEstimator, TransformerMixin):
    def __init__(self, old_name, new_name):
        self.old_name = old_name
        self.new_name = new_name

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X.rename(columns={self.old_name: self.new_name}, inplace=True)
        return X


# This class drops the first 18 columns of the DataFrame.
class ColumnDropper(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Drop the first 18 columns of the DataFrame
        columns_to_delete = list(range(0,18))
        return X.drop(X.columns[columns_to_delete], axis=1)
    

# This class changes the order of columns
class OrderChanger(BaseEstimator, TransformerMixin):
    def __init__(self, new_column_order):
        self.new_column_order = new_column_order

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X[self.new_column_order]

# Define the pipelines
tpipe = Pipeline([
    ("ddropper", DataDropper()),
    ("creater", ColumnCreater()),
    ("column_renamer", ColumnRenamer(old_name="Deutschland", new_name="Temperature (°C)")),
    ("cdropper", ColumnDropper()),
    ("ochanger", OrderChanger(new_column_order=["Date", "Temperature (°C)"]))
])

ppipe = Pipeline([
    ("ddropper", DataDropper()),
    ("creater", ColumnCreater()),
    ("column_renamer", ColumnRenamer(old_name="Deutschland", new_name="Precipitation (l/m²)")),
    ("cdropper", ColumnDropper()),
    ("ochanger", OrderChanger(new_column_order=["Date", "Precipitation (l/m²)"]))
])

# Applying the transformations in loops
for i in range(len(temp_data)):
    temp_data[i] = tpipe.fit_transform(temp_data[i])
    pre_data[i] = ppipe.fit_transform(pre_data[i])

# Merging the DataFrames in loops
list_temp = ["Date", "Temperature (°C)"]
list_precip = ["Date", "Precipitation (l/m²)"]

temp = temp_data[0]
pre = pre_data[0]

for i in range(1, len(temp_data)):
    temp = temp.merge(temp_data[i], on=list_temp, how="outer")
    pre = pre.merge(pre_data[i], on=list_precip, how="outer")

# Sorting the DataFrames
temp = temp.sort_values(by=["Date"], ignore_index=True)
pre = pre.sort_values(by=["Date"], ignore_index=True)

# Merging the DataFrames
wt = temp.merge(pre, on='Date', how="outer")


# Merging all the data

# Merge the four DataFrames ('fp', 'bop', 'ep', 'exp') on the 'Date' column using outer joins
df = fp.merge(bop, on='Date', how='outer')
df = df.merge(ep, on='Date', how='outer')
df = df.merge(exp, on='Date', how='outer')

# Check if the 'abbr' variable is equal to 'DE' (Germany)
if eu_abbr == 'DE':
    # If 'abbr' is 'DE', merge 'wt' DataFrame on the 'Date' column using an outer join
    df = df.merge(wt, on='Date', how='outer')



df = df.replace({None: np.nan})

st.dataframe(df)