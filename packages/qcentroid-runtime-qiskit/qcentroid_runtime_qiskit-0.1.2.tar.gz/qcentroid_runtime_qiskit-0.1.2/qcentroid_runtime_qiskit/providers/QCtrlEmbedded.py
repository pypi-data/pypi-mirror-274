from .QiskitRuntimeAbstractProvider import QiskitRuntimeAbstractProvider
from qiskit_ibm_runtime import QiskitRuntimeService

class QCtrlEmbedded(QiskitRuntimeAbstractProvider):
    def get_provider(self):
        return "QCtrlEmbedded"
    def _get_service(self):
        if(self._service is not None):
            return self._service
        params=self._get_params()
        if "QCtrlEmbeddedToken" in params:
            self.__token = params.get("QCtrlEmbeddedToken", "")
        else:
           raise Exception("No token provided") 
        if "QCtrlEmbeddedInstance" in params:
            self.__instance = params.get("QCtrlEmbeddedInstance", "")
        else:
           raise Exception("No instance provided") 
        self._service=  QiskitRuntimeService(channel='ibm_quantum',token=self.__token,instance=self.__instance)
        return self._service

