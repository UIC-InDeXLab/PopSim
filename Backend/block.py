from abstract_class import Unit
from utils import getDecennialData, getFIPS

class BlockByFIPS(Unit):
    def __init__(self, FIPS, censusYear = "2020"):  
      super().__init__("Block")
      if (len(FIPS) != 15):
          raise Exception("fips length is invalid")
      self._FIPS = FIPS
      self._censusYear = censusYear

    @property
    def decennialData(self):
        if(self._decennial_data is None):
            self._decennial_data = getDecennialData(self._FIPS, year = self._censusYear)
        return self._decennial_data

class BlockByLoc(BlockByFIPS):
    def __init__(self, lat, lon, censusYear = "2020"):  
        FIPS = getFIPS(lat, lon, year = censusYear)
        super().__init__(FIPS, censusYear)
    

