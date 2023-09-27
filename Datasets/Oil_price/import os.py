import os
import pandas as pd


path = os.getcwd()
brent_file = pd.read_csv('Brent.csv')

print(path)
print(brent_file)
