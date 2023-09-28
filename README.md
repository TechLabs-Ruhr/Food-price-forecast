# Food-Prices across Europe: An exploratory analysis tool
The following README is divide into two parts:

1. [Eurostat Data Analysis](#eurostat-data-analysis)

2. [XGB Regressor Model - Forecast](#xgb-regressor-model---forecast)

## Repository

- [Analysis Tool](Analysis_Tool.ipynb) - Instruction: [Part1](#usage-of-the-eurostat-data-query) / [Part2](#usage-of-the-xgb-regressor-model) - final project
- [Data set for the oil price](Datasets/Oil_price/Brent.csv)
- [Data sets for the precipitation](Datasets/Weather_data/Precipitation)
- [Data sets for the temperature ](Datasets/Weather_data/Temperature)
- [Weather Data Pipeline - First Version](Datasets/Weather_data/weather_data_pipeline.ipynb)
- [Link collection](Link_collection.md) <br>
<br>

The following files did not make it into the final project, but were kept for future enhancements:

- [Granger Causality Test](Granger_Causality_Impulse_Response_Function_updated.ipynb)
- [Forecast with LSTM](multivariate_LSTM_scaled_grid_search.ipynb)
- [Forecast with Sktime](Foodforecast_with_sktime.ipynb)




## Prerequisites
Before running the script, make sure you have the following libraries installed:
- `numpy`
- `pandas`
- `eurostat` (for Eurostat data retrieval)
- `easygui` (for creating simple GUIs)
- `matplotlib` (for data visualization)
- `seaborn` (for enhanced data visualization)
- `scikit-learn` (for machine learning)
- `xgboost` (for XGBoost machine learning model)
- `sktime` (for time series performance metrics)

<br>
<br>

# Eurostat Data Query
This Python script retrieves various economic and environmental data from Eurostat, a statistical office of the European Union, for further analysis. The data includes information on food prices, electricity prices, exchange rates, Brent oil prices, weather data, and optionally producer prices. The code allows users to select a specific EU country, food category, and producer prices (if needed). It then retrieves, cleans and integrates the data for analysis.

## Table of Contents
- [Usage of the Eurostat data query](#usage-of-the-eurostat-data-query)
- [Data Retrieval and Preprocessing](#data-retrieval-and-preprocessing)
- [Correlation Analysis](#correlation-analysis)

## Usage of the Eurostat data query
Run the script in a Python environment.
1. **Select a Country**: Upon running the code, a graphical input window will appear, allowing you to select a European country from the list.

2. **Select a Food Category**: After choosing a country, you'll be prompted to select a food category from a list of options. The code retrieves food price data specific to the chosen category for your selected country.

3. **Query Additional Data**: The code also queries additional economic and environmental data sources, including electricity prices, exchange rates, and producer prices, based on the selected country.

4. **Visualize Data**: The code merges all the retrieved data into a single DataFrame and calculates correlations between variables. It then generates a heatmap to visualize the relationships between different economic and environmental factors.

5. **User Interface**: The code utilizes the easygui library to provide a user-friendly interface for selecting countries and food categories. Follow the on-screen instructions to make selections.

**Note**: Depending on the selected country, some data sources may not be available or relevant. The code handles this by merging only relevant data for the selected country.


## Data Retrieval and Preprocessing
The script retrieves data from various sources, including Eurostat and external CSV files. It performs the following steps for data retrieval and preprocessing:

- Data retrieval for food prices, electricity prices, exchange rates, and producer prices.
- Data cleaning and formatting.
- Merging data from different sources based on the 'Date' column.
- Reshaping data as needed for analysis.

## Correlation Analysis
The script calculates correlations between different variables, including food prices, electricity prices, exchange rates, weather data (if applicable), and producer prices (if selected). It generates a correlation heatmap to visualize these relationships.

<br>
<br>
<br>


# XGB Regressor Model - Forecast
In the second part, an XGBoost (XGB) regressor model is used for univariate time series prediction of food prices. <br>
The XGBoost regressor model is designed for univariate time series prediction of food price indices. It enables forecasting future values of the food price index with configurable options.

## Table of Contents
- [Usage of the XGB Regressor Model](#usage-of-the-xgb-regressor-model)
- [Adjustment of the Data Frame](#adjustment-of-the-data-frame)
- [Setting up the Estimators for the Pipeline](#setting-up-the-estimators-for-the-pipeline)
- [Model Training](#model-training)
- [Postprocessing](#postprocessing)
- [Application of the Pipeline](#application-of-the-pipeline)

## Usage of the XGB Regressor Model
Run the script in a Python environment.
1. **Run the Code**: To use the XGBoost regressor model, simply run the code.

2. **Configuration**: The code provides an interactive configuration step that allows users to set various parameters, such as lower and upper boundaries for outlier removal, enabling or disabling cross-validation, specifying the number of splits for time series cross-validation, setting the test size, and defining a split time for separating training and testing data.

3. **Model Training**: The code preprocesses the data, removes outliers, creates features, and trains the XGBoost model.

4. **Model Evaluation**: It displays the model's predictions alongside the original data, calculates the Mean Absolute Percentage Error (MAPE), and Mean Squared Percentage Error (MSPE) for evaluation.

By following these steps, you can use the code to explore economic and environmental data or train an XGBoost regressor model for univariate time series prediction of food price indices.

## Adjustment of the Data Frame
The code starts by adjusting the input data frame to prepare it for modeling. Specifically:

- It renames the relevant column to 'FoodPriceIndex' for consistency.
- It checks for missing values in the data. If missing values are found, it displays a message.

## Setting up the Estimators for the Pipeline

The code defines several custom transformers as part of the data preprocessing pipeline. Depending on the wanted analysis parts of the pipeline can be commented out. The transformers perform various tasks:

- `ConvertDateTime`: Converts the date column to a datetime format.
- `DropPost21`: Filters data entries beyond a certain date (post-2021-11 in this case).
- `PlotPreData`: Plots the original data for visualization.
- `ShowOutliers`: Identifies and displays data points that are outliers.
- `RemoveOutliers`: Removes outliers from the data.
- `AbsDiffData`: Computes the absolute differences between consecutive data points.
- `CrossValidationSplit`: Splits the data for cross-validation and optionally displays the splits.
- `CreateFeatures`: Adds time-based features to the data.

## Model Training

The code defines a custom transformer `TrainModel` responsible for training the XGBoost regressor model. It offers two modes of operation:

- Cross-validation mode (`use_cv=True`): The data is split into multiple folds for cross-validation, and the model is trained and evaluated for each fold. The code calculates and prints the mean squared error (MSE) for each fold.
- Single split mode (`use_cv=False`): The data is split into a training set and a test set based on the specified split time. The model is trained on the training set and evaluated on the test set.

The XGBoost model hyperparameters can be further tuned and optimized based on your specific use case.


## Postprocessing

The code defines a custom transformer `ShowResults` for postprocessing and evaluation. It computes and displays the following:

- Cumulative predictions based on the model's output.
- Plots of the original data and predictions.
- Mean Absolute Percentage Error (MAPE) and Mean Squared Percentage Error (MSPE) as evaluation metrics.


## Application of the Pipeline

The code provides a configuration section where you can customize various parameters:

- Lower and upper boundaries for outlier detection.
- Whether to use cross-validation (`use_cv`) and whether to show cross-validation splits (`show_cv_split`).
- Number of splits and test size for cross-validation.
- The split time for separating training and test data.
- enable the option to "look into the future": this uses a framework that can also be used to look into the future, but it is currently hard coded to make a prediction for the time after 2021 that is in the following plotted to see the big influence of the ukraine war on the quality of the prediction

After configuring the parameters, the code runs the data through the defined pipeline, which includes data preprocessing, model training, and evaluation.

## Running the Code

To use this code:

1. Configure the parameters in the configuration section to match your use case.
2. Run the code to preprocess the data, train the model, and evaluate its performance.
3. Examine the results, including plots and evaluation metrics such as MAPE and MSPE.

<br>
<br>
<br>

# Outlook
* The code includes custom transformers and a preprocessing pipeline for handling weather data (temperature and precipitation) for Germany. This part of the code may be extended or modified for other countries.
* The code currently supports the XGBoost regressor model. In the future, it can be extended to include other machine learning models such as sktime or LSTM, which were also tested and can be found in the repository. They were not yet added to the pipeline.
* The code is currently set up for only a univariate prediction. A multivariate time series prediction may be added. 
* Presently there is no option to grid search for hyperparameter tuning. We tested this method in combination with the LSTM-Model but it is not yet part of the pipeline.
