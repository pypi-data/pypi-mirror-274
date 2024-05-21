import sys
import logging
import os
logger = logging.getLogger(__name__)
__all__=['providers']

import qcentroid_runtime_qiskit.providers as providers

class QCentroidRuntimeQiskit:
    _singleton = None

    @staticmethod
    def getVersion() -> str:
        # compatible with python 3.7 version
        if sys.version_info >= (3, 8):
            from importlib import metadata
        else:
            import importlib_metadata as metadata

        if __name__:
            return metadata.version(__name__)

        return "unknown"

    def __get_provider(self,params):
        provider_name=params.get("provider","IBMQuantum")
        if provider_name == 'IBMQuantum':
            self.__provider=providers.IBMQuantum(params)
        elif provider_name == 'IBMCloud':
            self.__provider=providers.IBMCloud(params)
        elif provider_name == 'QCtrlEmbedded':
            self.__provider=providers.QCtrlEmbedded(params)
        elif provider_name == 'IonQ':
            self.__provider=providers.IonQ(params)
        
        

    def __init__(self, params):
        self.__get_provider(params)
        

    @classmethod
    def get_instance(cls, params: dict = {}):
        if cls._singleton is None:
            cls._singleton = cls(params)
        return cls._singleton

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(QCentroidRuntimeQiskit, cls).__new__(cls)
        return cls._singleton
    @classmethod
    def execute(cls, circuit):
        self = cls.get_instance()
        return self.__provider.execute(circuit)


    
__all__ = ["QCentroidRuntimeQiskit"]
