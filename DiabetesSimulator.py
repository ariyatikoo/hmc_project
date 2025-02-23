from datetime import datetime, timedelta
from Patient import Patient

class DiabetesSimulator:
    
    def __init__(self, patient: Patient, starting_glucose: float = 110):
        self.patient = patient
        self.current_glucose = starting_glucose

        self.active_basal = [] # contains basal history
        self.meal_history = [] # list of all meals eaten
        self.active_carbs = [] # stores current active carbs
        self.active_bolus = [] # stores current active bolus (assume works in tandem with active_carbs)

        self.glucose_history = [starting_glucose]
        self.start_time = datetime.now()
        self.current_time = self.start_time

    def simulate(self, days=14, timesteps=5):
        total_steps = days * 24 * 60 // timesteps 

        for _ in range(total_steps):
            basal_in_five_mins = self.patient.basal_rate / 12
            self.active_basal.append(basal_in_five_mins)

            previous_glucose = self.glucose_history[-1]
            glucose_change = 0

            for basal in self.active_basal:
                glucose_change -= basal  
            
            for carbs in self.active_carbs:
                glucose_change += carbs  # naive approach: update glucose change based on how much would increase in 5 min timesteps, 
                #based on carbs eaten, distribute across 5 hrs
            
            for bolus in self.active_bolus:
                glucose_change -= bolus # hypothetically, cancels out all glucose increases from carb consumption 
            

            new_glucose = previous_glucose + glucose_change
            self.glucose_history.append(new_glucose)
        
            self.current_time = self.current_time + timedelta(minutes=5)
    
    def refresh(self):

        # N(t) = Nnull (0.5)^(t/81), where N is amount of insulin remaining, Nnull is amount of initial insulin, t is time passed
        # if final N is less than = 0.1 or small carb value, delete meal instance

        '''
        same for carbs, just not same half life value
        incorporate randomness in glycemic index values

        update active_insulin and active_meal

        1. we use half life function to determine how much insulin/carb remaining in 5 minutes
        2. subtract from how much currently remaining, shows how much glucose will change in 5 mins

        '''

        # carbs
        initial_carbs = 0
        t = self.current_time
        half_life = 1 # substitute in for actual half life of carbs
        final_carbs = initial_carbs * pow(0.5, (t/half_life))

        oldest_carbs = self.active_carbs[0]

        if (final_carbs <= 0.1) :
            self.active_carbs.remove(oldest_carbs) # remove oldest value in active_carbs once insulin is minimal

        # insulin
        initial_insulin = 0
        
        final_insulin = initial_insulin * pow(0.5, (t/81))

        oldest_insulin = self.active_bolus[0]

        if (final_insulin <= 0.1) :
            self.active_bolus.remove(oldest_insulin) 

       
       

        # delete meal history and active insulin older than 5 hrs

    # calc_insulin_impact  --> combine each impact
    # calc_meal_impact

# can edit to include bolus, meal management, and insulin decay