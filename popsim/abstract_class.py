from operator import index
from utils import getDecennialData
from abc import ABC, abstractmethod
import matplotlib as plt
import pandas as pd
import numpy as np
from utils import randomize_location, getSFDF
import os
import random
import requests

class Person():
    def __init__(self, blockFIPS, race, location=None):
        self._blockFIPS = blockFIPS
        self._race = race
        self._location = location

    @property
    def blockFIPS(self):
        return self._blockFIPS

    @property
    def race(self):
        return self._race

    @property
    def location(self):
        if (self._location is None):
            print(getDecennialData(self._blockFIPS, dataField="TRISUBREM"))
        return self._location

    @location.setter
    def censusYear(self, location):
        self._location = location

    def __repr__(self):
        return f"<Person block_FIPS:{self._blockFIPS}, race:{self._race}, location:{self.location}>"


class UnitInterface(ABC):

    def __init__(self):
        pass

    @property
    @abstractmethod
    def FIPS(self):
        pass

    @property
    @abstractmethod
    def censusYear(self):
        pass

    @property
    @abstractmethod
    def decennialData(self):
        pass

    @property
    @abstractmethod
    def decennialDataCumulative(self):
        pass

    @abstractmethod
    def getSample(self):
        pass

    @abstractmethod
    def graphDecennialData(self):
        pass


class Unit(UnitInterface):

    def __init__(self, administrativeUnit):
        self._administrative_unit = administrativeUnit
        self._group = None
        self._FIPS = None
        self._censusYear = None
        self._decennial_data = None
        self._decennial_data_cumulative = None
        self._shapeInfo = None
        self._otherData = None

    @property
    def administrativeUnit(self):
        return self._administrative_unit

    @property
    def FIPS(self):
        return self._FIPS

    @FIPS.setter
    def FIPS(self, fips):
        self._FIPS = fips

    @property
    def censusYear(self):
        return self._censusYear

    @censusYear.setter
    def censusYear(self, censusYear):
        self._censusYear = censusYear

    @property
    def decennialData(self):
        return self._decennial_data

    @decennialData.setter
    def decennialData(self, decennial_data):
        self._decennial_data = decennial_data

    @property
    def group(self):
        if (self._group is None):
            self._group = [
                'P1_003N', 'P1_004N', 'P1_005N', 'P1_006N', 'P1_007N',
                'P1_008N', 'P1_011N', 'P1_012N', 'P1_013N', 'P1_014N',
                'P1_015N', 'P1_016N', 'P1_017N', 'P1_018N', 'P1_019N',
                'P1_020N', 'P1_021N', 'P1_022N', 'P1_023N', 'P1_024N',
                'P1_025N', 'P1_027N', 'P1_028N', 'P1_029N', 'P1_030N',
                'P1_031N', 'P1_032N', 'P1_033N', 'P1_034N', 'P1_035N',
                'P1_036N', 'P1_037N', 'P1_038N', 'P1_039N', 'P1_040N',
                'P1_041N', 'P1_042N', 'P1_043N', 'P1_044N', 'P1_045N',
                'P1_046N', 'P1_048N', 'P1_049N', 'P1_050N', 'P1_051N',
                'P1_052N', 'P1_053N', 'P1_054N', 'P1_055N', 'P1_056N',
                'P1_057N', 'P1_058N', 'P1_059N', 'P1_060N', 'P1_061N',
                'P1_062N', 'P1_064N', 'P1_065N', 'P1_066N', 'P1_067N', 
                'P1_068N', 'P1_069N', 'P1_071N'
            ]
        return self._group

    @group.setter
    def group(self, group):
        self._group = group
        self._decennial_data_cumulative = None

    def setGroup(self, group):
        self._group = group
        self._decennial_data_cumulative = None
        return self

    @property
    def shapeInfo(self):
        if (self._shapeInfo is None):
            self._shapeInfo = getSFDF(
                self._FIPS, for_unit=self._administrative_unit).iloc[0]
        return self._shapeInfo

    @shapeInfo.setter
    def shapeInfo(self, shapeInfo):
        self._shapeInfo = shapeInfo

    def setShapeInfo(self, shapeInfo):
        self._shapeInfo = shapeInfo
        return self

    @property
    def decennialDataCumulative(self):
        if (self._decennial_data_cumulative is None):
            decennial_data_processed = pd.to_numeric(
                self.decennialData.get(self.group))
            decennial_data_processed = decennial_data_processed[
                decennial_data_processed > 0]
            if (decennial_data_processed.size == 0):
                print('No Population')
            self._decennial_data_cumulative = decennial_data_processed.cumsum()
            self._decennial_data_cumulative = self._decennial_data_cumulative * 1.0 / self._decennial_data_cumulative.max(
            )
        return self._decennial_data_cumulative

    @decennialDataCumulative.setter
    def decennialDataCumulative(self, decennial_data_cumulative):
        self._decennial_data_cumulative = decennial_data_cumulative

    def __repr__(self):
        return f"<Unit administrative_unit:{self._administrative_unit}, \n    FIPS:{self._FIPS}, \n    decennial_data: \n {self.decennialData}>"

    
    def getSample(self, n=1, to_csv=False):
        filename = self._FIPS + "_num-sample-" + str(n) + ".csv"
        pathfile = os.path.join("./data/generatedDatasets", filename)
        
        if (os.path.exists(pathfile)):
            return pd.read_csv(pathfile).iloc[:,1:]
        
        randomFloat = np.random.random_sample(size=n)
        indexNum = self.decennialDataCumulative.searchsorted(randomFloat,
                                                             side="right")
        if (sum(self.decennialDataCumulative) == 0):
            return []
        geometry = self.shapeInfo["geometry"]
        randomLocations = randomize_location(n, geometry)

        # income
        # extract median household income data and remove the header row
        header = data[0]
        data = data[1:]
        median_incomes = [float(row[header.index('B19013_001E')]) for row in data]
        # set base URL and parameters
        base_url = 'https://api.census.gov/data/2019/acs/acs5'
        params = {
            'get': 'NAME,B19013_001E',
            'for': f'block group:{self._FIPS[11:12]}',
            'in': [f'state:{self._FIPS[:2]}', f'county:{self._FIPS[2:5]}', f'tract:{self._FIPS[5:11]}'],
        }

        # make the request and get the response data
        response = requests.get(base_url, params=params)
        data = response.json()
        print("data: ", data)
        # # find values with same median income as n
        
        # # select a random value with the same median income as n
        random_value = random.choice(n)

        # print(random_value)

        df = pd.DataFrame({
            "FIPS": [self._FIPS] * n,
            "race":
            list(map(lambda x: self.decennialDataCumulative.index[x],
                     indexNum)),
            "lon":
            [loc.x for loc in randomLocations],
            "lat":
            [loc.y for loc in randomLocations]
        })
        
        if (to_csv):
            df.to_csv(pathfile)
        
        return df

    def graphDecennialData(self):
        self.getProcessedDecennialData()
        self._decennial_data.plot(kind='bar')
        plt.show()


class UnitByDecennialData(Unit):

    def __init__(self,
                 decennialData,
                 cummulativeDecennialData=None,
                 shapeInfo=None):
        if not isinstance(decennialData, pd.Series):
            raise ("The DecennialData must be a panda Series")
        self._FIPS = decennialData.GEO_ID[decennialData.GEO_ID.find('US') + 2:]
        if len(self._FIPS) == 2:
            self._administrative_unit = 'state'
        elif len(self._FIPS) == 5:
            self._administrative_unit = 'county'
        elif len(self._FIPS) == 11:
            self._administrative_unit = 'tract'
        elif len(self._FIPS) == 15:
            self._administrative_unit = 'block'
            
        self._censusYear = None
        self._group = None
        self._decennial_data = decennialData
        self._shapeInfo = shapeInfo
        self._decennial_data_cumulative = cummulativeDecennialData


class Group(UnitInterface):

    def __init__(self, FIPS, group_level, unit_level, census_year="2020"):
        self._administrative_unit = group_level
        self._FIPS = FIPS
        self._unit_level = unit_level
        self._censusYear = census_year
        self._decennial_data = None
        self._decennial_data_cumulative = None
        self._group = None
        self._shapeInfo = None

    @property
    def administrativeUnit(self):
        return self._administrative_unit

    @property
    def FIPS(self):
        return self._FIPS

    @FIPS.setter
    def FIPS(self, fips):
        self._FIPS = fips

    @property
    def censusYear(self):
        return self._censusYear

    @censusYear.setter
    def censusYear(self, censusYear):
        self._censusYear = censusYear

    @property
    def decennialData(self):
        return self._decennial_data

    @decennialData.setter
    def decennialData(self, decennial_data):
        self._decennial_data = decennial_data

    @property
    def group(self):
        if (self._group is None):
            self._group = [
                'P1_003N', 'P1_004N', 'P1_005N', 'P1_006N', 'P1_007N',
                'P1_008N', 'P1_011N', 'P1_012N', 'P1_013N', 'P1_014N',
                'P1_015N', 'P1_016N', 'P1_017N', 'P1_018N', 'P1_019N',
                'P1_020N', 'P1_021N', 'P1_022N', 'P1_023N', 'P1_024N',
                'P1_025N', 'P1_027N', 'P1_028N', 'P1_029N', 'P1_030N',
                'P1_031N', 'P1_032N', 'P1_033N', 'P1_034N', 'P1_035N',
                'P1_036N', 'P1_037N', 'P1_038N', 'P1_039N', 'P1_040N',
                'P1_041N', 'P1_042N', 'P1_043N', 'P1_044N', 'P1_045N',
                'P1_046N', 'P1_048N', 'P1_049N', 'P1_050N', 'P1_051N',
                'P1_052N', 'P1_053N', 'P1_054N', 'P1_055N', 'P1_056N',
                'P1_057N', 'P1_058N', 'P1_059N', 'P1_060N', 'P1_061N',
                'P1_062N', 'P1_063N', 'P1_064N', 'P1_065N', 'P1_066N',
                'P1_067N', 'P1_068N', 'P1_069N', 'P1_071N'
            ]
        return self._group

    @group.setter
    def group(self, group):
        self._group = group
        self._decennial_data_cumulative = None

    def setGroup(self, group):
        self._group = group
        self._decennial_data_cumulative = None
        return self

    @property
    def shapeInfo(self):
        if (self._shapeInfo is None):
            self._shapeInfo = getSFDF(self._FIPS, for_unit=self._unit_level)
        return self._shapeInfo

    @shapeInfo.setter
    def shapeInfo(self, shapeInfo):
        self._shapeInfo = shapeInfo
    
    @property
    def Units(self):
        return self._units

    @property
    def decennialDataCumulative(self):
        if (self._decennial_data_cumulative is None):
            decennial_data_processed = self.decennialData[self.group]
            decennial_data_processed = decennial_data_processed.apply(
                pd.to_numeric, errors='ignore')

            print(decennial_data_processed)
            decennial_data_processed = decennial_data_processed.sum(axis=1)
            decennial_data_processed.index = map(
                str, decennial_data_processed.index)
            decennial_data_processed = decennial_data_processed[
                decennial_data_processed > 0]
            print(decennial_data_processed)
            if (decennial_data_processed.size == 0):
                print('No Population')
            self._decennial_data_cumulative = decennial_data_processed.cumsum()
            self._decennial_data_cumulative = self._decennial_data_cumulative * 1.0 / self._decennial_data_cumulative.max(
            )
        return self._decennial_data_cumulative

    @decennialDataCumulative.setter
    def decennialDataCumulative(self, decennial_data_cumulative):
        self._decennial_data_cumulative = decennial_data_cumulative

    def __repr__(self):
        return f"<Group administrative_unit:{self._administrative_unit}, \n element_unit:{self._unit_level}, \n     FIPS:{self._FIPS}, \n    decennial_data: \n {self.decennialData}>"

    def getSample(self, n=1, group=None, to_csv=False, name=None):
        if name is None:
            filename = self._administrative_unit + "_"+ self._FIPS + "_by_" + self._unit_level+ "_num_people_" + str(n) +".csv"
        else:
            filename = name
        pathfile = os.path.join("./data/generatedDatasets", filename)
        
        if (os.path.exists(pathfile)):
            return pd.read_csv(pathfile).iloc[:,1:]
        
        randomFloat = np.random.random_sample(size=n)
        indexNum = self.decennialDataCumulative.searchsorted(randomFloat, side="right")
        indexes, num_people = np.unique(indexNum, return_counts=True)
        decennial_data_indexes = list(map(lambda x: self.decennialDataCumulative.index[x], indexes))
        sample = []
        
        for i in range(len(decennial_data_indexes)):
            print(num_people[i])
            decennial_data_row = self.decennialData.iloc[int(decennial_data_indexes[i])]
            shapeInfo_row = self.shapeInfo[self.shapeInfo.GEOID == decennial_data_row.GEO_ID[decennial_data_row.GEO_ID.find('US') + 2:]].iloc[0]
            sample.append(UnitByDecennialData(decennial_data_row).setGroup(self.group).setShapeInfo(shapeInfo_row).getSample(num_people[i]))
            
        sample = pd.concat(sample)
        
        if(to_csv): 
            sample.to_csv(pathfile)
            
        return sample

    def graphDecennialData(self):
        self.getProcessedDecennialData()
        self._decennial_data.plot(kind='bar')
        plt.show()
