from block import BlockByFIPS
from state import StateByBlockGroup;
import pandas as pd

# df = BlockByFIPS("170318371002012").getSample(5000, to_csv=True)
df = StateByBlockGroup("17").getSample(50, to_csv=True)
print(df)