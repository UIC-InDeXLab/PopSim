from typing import Union

from fastapi import FastAPI

from state import StateByBlockGroup
from tract import TractByBlockGroup
from block import BlockByFIPS
app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/get_sample_by_fips/{level}/{fips}/{num}")
def read_sample_by_fips(level: str, fips: str, num: int):
    if (level == "state") :
        return {"level": level, "fips":fips, "sample": StateByBlockGroup(fips).getSample(num)} 
    elif (level == "tract"):
        return {"level": level, "fips":fips, "sample": TractByBlockGroup(fips).getSample(num)}
    elif (level == "block"):
        return {"level": level, "fips":fips, "sample": BlockByFIPS(fips).getSample(num)}