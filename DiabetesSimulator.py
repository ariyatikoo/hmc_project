from datetime import datetime
from Patient import Patient

class DiabetesSimulator:
    
    def __init__(self, patient: Patient, starting_glucose: float = 110):
        self.patient = patient
        self.current_glucose = starting_glucose
        self.active_insulin = []
        self.meal_history = []
        self.glucose_history = [starting_glucose]
        self.start_time = datetime.now()
        self.current_time = datetime.now()

    def simulate(self, days=14, timesteps=5):
        total_steps = days * 24 * 60 // timesteps 

        for _ in range(total_steps):
            basal_in_five_mins = self.patient.basal_rate / 12
            self.active_insulin.append(basal_in_five_mins)

            previous_glucose = self.glucose_history[-1]
            glucose_change = 0

            for insulin in self.active_insulin:
                glucose_change -= insulin  
            
            for meal in self.meal_history:
                glucose_change += meal  

            new_glucose = previous_glucose + glucose_change
            self.glucose_history.append(new_glucose)
            
# can edit to include bolus, meal management, and insulin decay