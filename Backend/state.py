from abstract_class import Unit, Group
from utils import getDecennialData, getFIPS

class StateByFIPS(Unit):
    def __init__(self, FIPS, censusYear = "2020"):  
      super().__init__("State")
      if (len(FIPS) != 2):
          raise Exception("fips length is invalid")
      self._FIPS = FIPS
      self._censusYear = censusYear

    @property
    def decennialData(self):
        if(self._decennial_data is None):
            self._decennial_data = getDecennialData(self._FIPS, year = self._censusYear, for_unit="state")
        return self._decennial_data

class StateByLoc(StateByFIPS):
    def __init__(self, lat, lon, censusYear = "2020"):  
        FIPS = getFIPS(lat, lon, year = censusYear, division="State")
        super().__init__(FIPS, censusYear)

class StateByBlockGroup(Group):
    def __init__(self, FIPS, census_year = "2020"):
        if (len(FIPS) != 2):
            raise Exception("fips length is invalid")
        super().__init__(FIPS, group_level = "State", unit_level = "Block", census_year = census_year)

    @property
    def decennialData(self):
        if(self._decennial_data is None):
            self._decennial_data = getDecennialData(self._FIPS,  for_unit = 'block', year = self._censusYear)
        return self._decennial_data