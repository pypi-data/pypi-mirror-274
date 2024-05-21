from .QiskitRuntimeAbstractProvider import QiskitRuntimeAbstractProvider
from qiskit_ibm_runtime import QiskitRuntimeService

class IBMCloud(QiskitRuntimeAbstractProvider):
    def get_provider(self):
        return "IBMCloud"
    def _get_service(self):
        if(self._service is not None):
            return self._service
        params=self._get_params()
        if "IBMCloudToken" in params:
            self.__token = params.get("IBMCloudToken", "")
        else:
           raise Exception("No token provided") 
        if "IBMCloudInstance" in params:
            self.__instance = params.get("IBMCloudInstance", "")
        else:
           raise Exception("No instance provided") 
        self._service=  QiskitRuntimeService(channel='ibm_cloud',token=self.__token,instance=self.__instance)
        return self._service
