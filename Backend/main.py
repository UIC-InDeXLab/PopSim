from typing import Union

from fastapi import FastAPI

from state import StateByBlockGroup
from tract import TractByBlockGroup
from block import BlockByFIPS

description= """
This is the APi help create a data synthesis for population based on the Census Bureau data
"""
app = FastAPI(
    title="Population Synthesis",
    description=description,
    version="0.0.1",
    contact={
        "name": "Khanh Duy Nguyen",
        "url": "http://khanh-duy.com/",
        "email": "knguye71@uic.edu",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


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