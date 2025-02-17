class Patient:
    def __init__(self, patient_id, correction_factor, carb_ratio, basal_rate, target_bg):
        self.patient_id = patient_id
        self.correction_factor = correction_factor
        self.carb_ratio = carb_ratio
        self.basal_rate = basal_rate
        self.target_bg = target_bg

    def __str__(self):
        return (
            f"Patient: {self.patient_id}\n"
            f"Correction Factor: {self.correction_factor}\n"
            f"Carb Ratio: {self.carb_ratio}\n"
            f"Basal Rate: {self.basal_rate}\n"
            f"Target BG: {self.target_bg}\n"
        )
    
patient_1 = Patient(patient_id=1, correction_factor=50, carb_ratio=10, basal_rate=1.0, target_bg=110) 
print(patient_1)