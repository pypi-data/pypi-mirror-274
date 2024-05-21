from .QiskitRuntimeAbstractProvider import QiskitRuntimeAbstractProvider
from qiskit_ibm_runtime import QiskitRuntimeService

class IBMQuantum(QiskitRuntimeAbstractProvider):
    def get_provider(self):
        return "IBMQuantum"
    def _get_service(self):
        if(self._service is not None):
            return self._service
        params=self._get_params()
        if "IBMQuantumToken" in params:
            self.__token = params.get("IBMQuantumToken", "")
        else:
           raise Exception("No token provided") 
        if "IBMQuantumInstance" in params:
            self.__instance = params.get("IBMQuantumInstance", "")
        else:
           raise Exception("No instance provided") 
        self._service= QiskitRuntimeService(channel='ibm_quantum',token=self.__token,instance=self.__instance)
        return self._service



