from abstract_class import Unit, Group
from utils import getDecennialData, getFIPS

class TractByFIPS(Unit):
    def __init__(self, FIPS, censusYear = "2020"):  
      super().__init__("tract")
      if (len(FIPS) != 11):
          raise Exception("fips length is invalid")
      self._FIPS = FIPS
      self._censusYear = censusYear

    @property
    def decennialData(self):
        if(self._decennial_data is None):
            self._decennial_data = getDecennialData(self._FIPS, year = self._censusYear, for_unit="tract")
        return self._decennial_data

class TractByBlockGroup(Group):
    def __init__(self, FIPS, census_year = "2020"):
        if (len(FIPS) != 11):
            raise Exception("fips length is invalid")
        super().__init__(FIPS, group_level = "Tract", unit_level = "Block", census_year = census_year)

    @property
    def decennialData(self):
        if(self._decennial_data is None):
            self._decennial_data = getDecennialData(self._FIPS,  for_unit = 'block', year = self._censusYear)
        return self._decennial_data