from block import BlockByFIPS
from state import StateByBlockGroup, StateByFIPS;
import pandas as pd
import numpy as np

np.random.seed(2020202)

# df = BlockByFIPS("170318371002012").getSample(5000, to_csv=True)
for i in range(10,20):
    df = StateByBlockGroup("17").getSample(12812508, to_csv=True, name="IL_dataset_"+str(i))
# df = StateByBlockGroup("17").decennialData
# df = StateByFIPS("17").decennialData
print(df)