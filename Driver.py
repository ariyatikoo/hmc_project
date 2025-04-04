from DiabetesSimulator import DiabetesSimulator
from Patient import Patient

patient_1 = Patient(patient_id=1, correction_factor=50, carb_ratio=10, basal_rate=1.0, target_bg=110) 
mySimulation = DiabetesSimulator(patient_1)
mySimulation.run_simulation()