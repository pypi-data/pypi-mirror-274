from .QiskitAbstractProvider import QiskitAbstractProvider
try:
    from qiskit_ionq import IonQProvider
except:
    import sys
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qiskit-ionq'])
    from qiskit_ionq import IonQProvider
import json
class IonQ(QiskitAbstractProvider):
    def __init__(self,params):
        self.__params=params
        if "backend" in params:
           self.__backend_name = params.get("backend", "")  
        self._qcentroid_job_id = params.get("qcentroid_job_id", None) 

    def get_provider(self):
        return 'IonQ'
    def _get_backend(self):
        provider = IonQProvider(token=self.__params.get('IonQ_API_Key',""))
        backend=provider.get_backend(self.__backend_name)
        backend.options.noise_model=self.__params.get('IonQ_Noise_Model',"ideal")
        return backend
                                                        
    def execute(self,circuit):
        backend=self._get_backend()
        job=backend.run(circuit)
        ids={}
        ids['IonQ Job ID']=job.job_id()
        job.wait_for_final_state()
        if self._qcentroid_job_id is not None:
            with open(str(self._qcentroid_job_id), 'w') as convert_file: 
                convert_file.write(json.dumps(ids))
        return job.get_probabilities()

    
    