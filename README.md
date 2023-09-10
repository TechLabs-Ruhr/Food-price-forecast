# Food price forecast for Europe

3 different Models, up till now somewhat similar quality of results. multivariate model still has to be investigated.

Pipeline for data processing: 

one python file called forecast_main.py which includes:

- pipeline from jacob to preprocess data, with option to choose the name of the variable (column) that shall be processed and that clears data format. also there should be options (flags) for what shall be processed
- possible functions that could be added to the pipeline:
    
    1. remove outliers, depending on plots
    2. remove data after december 2021
    3. set test/training split
    4. choose option for model to train with
    5. choose option for building the diff (absolute or relative)
    6. set option for grid search
    7. choose different features
    8. plot result and show rmse and stuff




