from DiabetesSimulator import DiabetesSimulator
from Patient import Patient

patient_1 = Patient(patient_id=1, correction_factor=50, carb_ratio=10, basal_rate=1.0, target_bg=110, avrg_breakfast_carbs = 45, avrg_lunch_carbs = 55, avrg_dinner_carbs = 65) 
mySimulation = DiabetesSimulator(patient_1)
mySimulation.run_simulation()
mySimulation.writeCSV("TestBGFile_1.csv", "TestInsulinFile_1.csv")