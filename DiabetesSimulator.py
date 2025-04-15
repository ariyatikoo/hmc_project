from datetime import datetime, timedelta
from Patient import Patient
import matplotlib.pyplot as plt
import random
import csv

'''
where to introduce variance?
with gut glucose - maybe not
meal carbs
breakfast/dinner/lunch range, 15 to 90 grams of carbs for different people(create different patient profiles)
'''

class DiabetesSimulator:
    
    def __init__(self, patient: Patient, starting_bg: float = 110.0, starting_insulin: float = 0, starting_glucose =0):
        self.patient = patient

        # time
        self.start_time = datetime(2025,1,1,0,0)
        self.current_time = self.start_time
        # insulin
        self.current_insulin = starting_insulin

        # glucose 
        self.current_glucose = starting_glucose

        # bg
        self.current_bg = starting_bg

        # each time corresponds to all the glucose and insulin that occured between that time and 5 mins later, and then the final bg reading
        self.diabetes_dict = {self.current_time : [self.current_insulin, self.current_glucose, self.current_bg]} 
        # format- {time: insulin, liver glucose, blood glucose}


    def run_simulation(self, days=14, five_min_interval=5):

        IOB = []
        GOB = []
        bg_arr = []
      

        steps = days * 24 * 60 // five_min_interval # what steps is actually supposed to be
        steps = 288 # one day worth of steps
        delta = timedelta(minutes=5)
       
        b_day = 0
        l_day = 0
        d_day = 0
        bg = self.current_bg
        last_correction = self.current_time
        for _ in range(steps):

            if (bg < 40):
                bg = 70
            
            if (bg < 80 ):
                glucose = 15
                insulin = 0
                
            elif bg > 320:
                bg = 290
                
            elif bg > 250:
                glucose = 0
                
                

            else:           
                insulin = self.basal() 
                glucose = self.glucose_secretion() 

                # meals
                meal_insulin = 0
                carbs = 0

                if self.current_time.hour == 7 and self.current_time.day != b_day:
                    meal_insulin, carbs = self.addMealEvent('breakfast', bg, insulin)
                    b_day = self.current_time.day

                if self.current_time.hour == 12 and self.current_time.day != l_day:
                    meal_insulin, carbs = self.addMealEvent('lunch', bg, insulin)
                    l_day = self.current_time.day

                if self.current_time.hour == 19 and self.current_time.day != d_day:
                    meal_insulin, carbs = self.addMealEvent('dinner', bg, insulin)
                    d_day = self.current_time.day

                insulin += meal_insulin
                glucose += carbs

           

            if (self.current_time - last_correction).seconds/3600 > 1 :
                insulin += self.auto_correction(bg)
                last_correction = self.current_time     

            bg = round(bg, 0)
            bg_arr.append(bg)
            insulin =  round(insulin, 3)
            glucose = round(glucose, 3)
                
            self.diabetes_dict.update({self.current_time: [insulin, glucose, bg]})

            bg = self.update_bg() 
            self.current_time += delta

            active_insulin = 0
            active_glucose = 0

            for t, data in self.diabetes_dict.items():
                if ((self.current_time.timestamp() - t.timestamp())/3600 > 5):
                    continue
                active_insulin += data[0] - self.insulin_decay(data[0], t.timestamp(), self.current_time.timestamp()) 
            
            for t, data in self.diabetes_dict.items():
                if ((self.current_time.timestamp() - t.timestamp())/3600 > 5):
                    continue
                active_glucose += data[1] - self.glucose_decay(data[1], t.timestamp(), self.current_time.timestamp()) 

            IOB.append(active_insulin)
            GOB.append(active_glucose)

            
       

        for k, v in self.diabetes_dict.items():
            print(k, v)  

    def writeCSV(self, bg_file_name, insulin_file_name):
        cgm_headers = ["EventDateTime", "Readings (mg/dL)"]
        pump_headers = ["CompletionDateTime", "BG (mg/dL)", "InsulinDelivered", "CarbSize"]

        cgm_rows = []
        pump_rows = []

        for k, v in self.diabetes_dict.items():
            cgm_rows.append([k, v[2]])
            pump_rows.append([k, v[2], v[0], v[1]])
        
        with open(bg_file_name, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(cgm_headers)
            for row in cgm_rows:
                writer.writerow(row)
 
        with open(insulin_file_name, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(pump_headers)
            for row in pump_rows:
                writer.writerow(row)
        


      # helper methods just meant to update lists and preserve history
    def glucose_secretion(self):
        return (self.patient.basal_rate/12)
    
    
    def basal(self): 
        return (self.patient.basal_rate / 12)
    
   
    def auto_correction(self, bg):
            
            active_insulin = 0
            for t, data in self.diabetes_dict.items():
                if ((self.current_time.timestamp() - t.timestamp())/3600 > 5):
                    continue
                active_insulin += data[0] - self.insulin_decay(data[0], t.timestamp(), self.current_time.timestamp()) 
                
            correction = (max(0, ((bg  - 110)/self.patient.correction_factor) - active_insulin))
        
            if bg > 180:  
                return correction
            
            else:
                return 0
        
    
    def addMealEvent(self, meal_type, bg, insulin):
        if (meal_type == 'breakfast') :
            carbs = self.patient.breakfast_getter()
        if (meal_type == 'lunch'):
            carbs = self.patient.lunch_getter()
        if (meal_type == 'dinner'):
            carbs = self.patient.dinner_getter()
       
        
        meal_insulin = carbs/self.patient.carb_ratio

        active_insulin = 0

        for t, data in self.diabetes_dict.items():
            if ((self.current_time.timestamp() - t.timestamp())/3600 > 5):
                continue
            active_insulin +=  data[0] - self.insulin_decay(data[0], t.timestamp(), self.current_time.timestamp()) 

        insulin_reduction = ((110-bg)/self.patient.correction_factor) + active_insulin # insulin is IOB
        #correction =  max(0, (((bg-110)/self.patient.correction_factor) - active_insulin))

        if (bg < 110) :
            meal_insulin = meal_insulin - max(0, insulin_reduction)
        
        if (meal_insulin <0) :
            meal_insulin = 0
        '''
        if (bg > 110) :
            meal_insulin = meal_insulin + correction
        '''
        
        return meal_insulin, carbs
    
    
   
    # updating methods
   
    def update_bg(self):
        current_bg = self.diabetes_dict[self.current_time][2]
        future = self.current_time + timedelta(minutes=5)

        for t, data in self.diabetes_dict.items():
            if ((self.current_time.timestamp() - t.timestamp())/3600 > 5):
                continue
            active_insulin = self.insulin_decay(data[0], t.timestamp(), self.current_time.timestamp()) - self.insulin_decay(data[0], t.timestamp(), future.timestamp())
            active_glucose = self.glucose_decay(data[1], t.timestamp(), self.current_time.timestamp()) - self.glucose_decay(data[1], t.timestamp(), future.timestamp())
           
            current_bg -= active_insulin * self.patient.correction_factor
            current_bg += (active_glucose/self.patient.carb_ratio) * self.patient.correction_factor 

       

        return current_bg
      
    def insulin_decay(self, current_insulin, t0, t1):
        elapsed_time = (t1 - t0)
        elapsed_time = elapsed_time/60
        half_life = random.gauss(81,8) # in minutes
        current_insulin = current_insulin * pow(0.5, (elapsed_time/half_life))

        return current_insulin
    
    def glucose_decay(self, current_glucose, t0, t1):
        elapsed_time = (t1 - t0)
        elapsed_time = elapsed_time/60 
        half_life = random.gauss(50,5) # minutes
        current_glucose = current_glucose * pow(0.5, (elapsed_time/half_life))

        return current_glucose




 