
    
from abc import ABC, abstractmethod
import json

class QiskitAbstractProvider(ABC):
    @abstractmethod
    def get_provider(self):
        pass

    
    def __init__(self,params):
        self.__params=params
        if "backend" in params:
           self.__backend_name = params.get("backend", "") 

        self._qcentroid_job_id = params.get("qcentroid_job_id", None) 

    def _get_params(self):
        return self.__params

    @abstractmethod  
    def _get_backend(self):
        pass


    @abstractmethod  
    def execute(self,circuit):
        pass