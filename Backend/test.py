from block import BlockByFIPS
from state import StateByBlockGroup, StateByFIPS;
import pandas as pd
import numpy as np

np.random.seed(2020202)


StateByBlockGroup("17").getSample(5000000, to_csv=True, name="IL_dataset_5mil.csv")
StateByBlockGroup("17").getSample(1000000, to_csv=True, name="IL_dataset_1mil.csv")
StateByBlockGroup("17").getSample(500000, to_csv=True, name="IL_dataset_500thousand.csv")
StateByBlockGroup("17").getSample(200000, to_csv=True, name="IL_dataset_200thousand.csv")
StateByBlockGroup("17").getSample(50000, to_csv=True, name="IL_dataset_50thousand.csv")