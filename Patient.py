import random

class Patient:
    def __init__(self, patient_id, correction_factor, carb_ratio, basal_rate, target_bg, avrg_breakfast_carbs, avrg_lunch_carbs, avrg_dinner_carbs):
        self.patient_id = patient_id
        self.correction_factor = correction_factor
        self.carb_ratio = carb_ratio
        self.basal_rate = basal_rate
        self.target_bg = target_bg
        self.avrg_breakfast_carbs = avrg_breakfast_carbs
        self.avrg_lunch_carbs = avrg_lunch_carbs
        self.avrg_dinner_carbs = avrg_dinner_carbs

    def __str__(self):
        return (
            f"Patient: {self.patient_id}\n"
            f"Correction Factor: {self.correction_factor}\n"
            f"Carb Ratio: {self.carb_ratio}\n"
            f"Basal Rate: {self.basal_rate}\n"
            f"Target BG: {self.target_bg}\n"
            f"Average Breakfast Carbs: {self.avrg_breakfast_carbs}\n"
            f"Average Lunch Carbs: {self.avrg_lunch_carbs}\n"
            f"Average Dinner Carbs: {self.avrg_dinner_carbs}\n"
        )

    def breakfast_getter(self):
        pct_dev = 0.2 
        deviation_value = pct_dev * self.avrg_breakfast_carbs
        std_dev_exact = deviation_value/1.96 #z value = 1.96
        return round(max(0,(random.gauss(self.avrg_breakfast_carbs, std_dev_exact))),0)
    
    def lunch_getter(self):
        pct_dev = 0.2 
        deviation_value = pct_dev * self.avrg_lunch_carbs
        std_dev_exact = deviation_value/1.96 #z value = 1.96
        return round(max(0,(random.gauss(self.avrg_lunch_carbs, std_dev_exact))),0)
    
    
    def dinner_getter(self):
        pct_dev = 0.2 
        deviation_value = pct_dev * self.avrg_dinner_carbs
        std_dev_exact = deviation_value/1.96 #z value = 1.96
        return round(max(0,(random.gauss(self.avrg_dinner_carbs, std_dev_exact))),0)
    
    
patient_1 = Patient(patient_id=1, correction_factor=50, carb_ratio=10, basal_rate=1.0, target_bg=110, avrg_breakfast_carbs = 45, avrg_lunch_carbs = 55, avrg_dinner_carbs = 65) 
print(patient_1)

'''
print(patient_1.breakfast_getter())
print(patient_1.breakfast_getter())
print(patient_1.breakfast_getter())
print(patient_1.breakfast_getter())
print(patient_1.breakfast_getter())
print(patient_1.breakfast_getter())
print(patient_1.breakfast_getter())
print(patient_1.breakfast_getter())
print(patient_1.breakfast_getter())

print(patient_1.lunch_getter())
print(patient_1.lunch_getter())
print(patient_1.lunch_getter())
print(patient_1.lunch_getter())
print(patient_1.lunch_getter())

print(patient_1.dinner_getter())
print(patient_1.dinner_getter())
print(patient_1.dinner_getter())
print(patient_1.dinner_getter())
print(patient_1.dinner_getter())
'''