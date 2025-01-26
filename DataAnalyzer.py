# author name: Ariya F Tikoo


import pandas as pd
import sys
from datetime import datetime, timedelta
sys.path.append('/Users/aft/VisualStudioCodeWorkspace/Python')
from hmc_project.DataLoader import DataLoader # type: ignore


class DataAnalyzer(DataLoader):

    def __init__(self):
        super().__init__()
        self.summary = "generated from data analyzer"
    
    def calcBGmean(self, specified_date, time_frame):
        self.getBGDict()
        
        if time_frame == '1 day':
            bg_table = self.getBGforOneDay(specified_date)
        elif time_frame == '3 days':
            bg_table = self.getPast3DaysBg(specified_date)
        elif time_frame == '2 weeks':
            bg_table = self.getBGTable()
        else:
            raise ValueError("Choose '1 day', '3 days', or '2 weeks'.")
        
        bg_table['Readings (mg/dL)'] = pd.to_numeric(bg_table['Readings (mg/dL)'])
        bg_table = bg_table.dropna(subset=['Readings (mg/dL)'])
        return bg_table['Readings (mg/dL)'].mean()
       
    
    def calcBGmedian(self, specified_date, time_frame):
        self.getBGDict()
        
        if time_frame == '1 day':
            bg_table = self.getBGforOneDay(specified_date)
        elif time_frame == '3 days':
            bg_table = self.getPast3DaysBg(specified_date)
        elif time_frame == '2 weeks':
            bg_table = self.getBGTable()
        else:
            raise ValueError("Choose '1 day', '3 days', or '2 weeks'.")
        
        bg_table['Readings (mg/dL)'] = pd.to_numeric(bg_table['Readings (mg/dL)'])
        bg_table = bg_table.dropna(subset=['Readings (mg/dL)'])
        return bg_table['Readings (mg/dL)'].median()
    
    
    def BGtimeInRange(self, specified_date, time_frame, lower_bound=75, upper_bound=135):
        self.getBGDict()
        if time_frame == '1 day':
            bg_table = self.getBGforOneDay(specified_date)
        elif time_frame == '3 days':
            bg_table = self.getPast3DaysBg(specified_date)
        elif time_frame == '2 weeks':
            bg_table = self.getBGTable()
        else:
            raise ValueError("Choose '1 day', '3 days', or '2 weeks'.")

        # Ensure the column is numeric and drop invalid rows
        bg_table['Readings (mg/dL)'] = pd.to_numeric(bg_table['Readings (mg/dL)'], errors='coerce')
        bg_table = bg_table.dropna(subset=['Readings (mg/dL)'])  # Drop rows where conversion failed
        column_data = bg_table['Readings (mg/dL)']

        in_range = column_data[(column_data >= lower_bound) & (column_data <= upper_bound)]
        return (len(in_range) / len(column_data)) * 100

    
    def BGpercentHigh(self, specified_date, time_frame, high_bound=180):
        self.getBGDict()
        
        if time_frame == '1 day':
            bg_table = self.getBGforOneDay(specified_date)
        elif time_frame == '3 days':
            bg_table = self.getPast3DaysBg(specified_date)
        elif time_frame == '2 weeks':
            bg_table = self.getBGTable()
        else:
            raise ValueError("Choose '1 day', '3 days', or '2 weeks'.")

        bg_table['Readings (mg/dL)'] = pd.to_numeric(bg_table['Readings (mg/dL)'], errors='coerce')
        bg_table = bg_table.dropna(subset=['Readings (mg/dL)'])
        column_data = bg_table['Readings (mg/dL)']

        high_values = column_data[column_data >= high_bound]
        return (len(high_values) / len(column_data)) * 100
    
    def BGpercentLow(self, specified_date, time_frame, low_bound=75):
        self.getBGDict()
        
        if time_frame == '1 day':
            bg_table = self.getBGforOneDay(specified_date)
        elif time_frame == '3 days':
            bg_table = self.getPast3DaysBg(specified_date)
        elif time_frame == '2 weeks':
            bg_table = self.getBGTable()
        else:
            raise ValueError("Choose '1 day', '3 days', or '2 weeks'.")

        bg_table['Readings (mg/dL)'] = pd.to_numeric(bg_table['Readings (mg/dL)'], errors='coerce')
        bg_table = bg_table.dropna(subset=['Readings (mg/dL)'])
        column_data = bg_table['Readings (mg/dL)']

        low_values = column_data[column_data <= low_bound]
        return (len(low_values) / len(column_data)) * 100
    
    def getNumCorrections(self, column1_name='CorrectionDelivered', column2_name='InsulinDelivered', column3_name='FoodDelivered'):
        insulin_table = self.getInsulinTable()
        
        num_control_iq = (insulin_table[column1_name] != 0).sum()
        manual_corrections = ((insulin_table[column1_name] == 0) &
                              (insulin_table[column3_name] == 0) &
                              (insulin_table[column2_name] != 0)).sum()
        return num_control_iq + manual_corrections
    
   
    def checkNighttimeBasal(self, specific_date):
        self.getBGDict()

        nighttime_data = self.getNighttimeBg(specific_date)  

        # Calculate stats
        nighttime_mean = nighttime_data['Readings (mg/dL)'].mean()
        nighttime_median = nighttime_data['Readings (mg/dL)'].median()
        nighttime_tir = self.BGtimeInRange(specific_date, '1 day')

        
        # Debugging outputs
        #print(f"Nighttime Mean: {nighttime_mean}")
        #print(f"Nighttime Median: {nighttime_median}")
        #print(f"Nighttime Time In Range: {nighttime_tir}")
        

        # Determine basal adjustments
        if nighttime_mean > 110:
            if nighttime_mean > 130:
                return "Increase basal during 11pm to 5am by 0.15"
            if nighttime_mean > 150:
                return "Increase basal during 11pm to 5am by 0.2"
            if nighttime_mean > 170:
                return "Increase basal during 11pm to 5am by 0.25"
            if nighttime_mean > 190:
                return "Increase basal during 11pm to 5am by 0.3"
            return "Increase basal during 11pm to 5am by 0.1"
        elif nighttime_mean < 80 and nighttime_median < 80:
            return "Decrease basal during 11pm to 5am by 0.1"
        return "No changes needed."

    def checkDawnPhenonmenon(self, specific_date):
        self.getBGDict()
        morning_data = self.getMorningBg(specific_date) 
        
        if morning_data.empty:
            return "No morning data available for analysis."

        # Calculate stats
        morning_mean = morning_data['Readings (mg/dL)'].mean()

        #print("Morning BG Mean: ", morning_mean)
      
        # Determine basal adjustments
        if morning_mean > 140:
            if morning_mean > 160:
                return "Increase basal during 5am to 7am by 0.2"
            if morning_mean > 180:
                return "Increase basal during 5am to 7am by 0.3"
            if morning_mean > 200:
                return "Increase basal during 5am to 7am by 0.4"
            return "Increase basal during 5am to 7am by 0.1"

        return "No changes needed."



    def checkCarbRatio(self, specific_date):
       
        """
        Check carb ratio based on BG changes 3 hours after food bolus.
        """

        # 1. Fetch BG and Insulin Data as DataFrames
        self.getBGDict()
        self.getInsulinDict()
        bg = self.getPast3DaysBg(specific_date)  
        insulin = self.getPast3DaysInsulin(specific_date)  

        # Convert date columns to datetime
        bg['EventDateTime'] = pd.to_datetime(bg['EventDateTime'])
        insulin['CompletionDateTime'] = pd.to_datetime(insulin['CompletionDateTime'])
        
        
        # Convert BG and insulin values to numeric
        bg['Readings (mg/dL)'] = pd.to_numeric(bg['Readings (mg/dL)'])
        insulin['BG (mg/dL)'] = pd.to_numeric(insulin['BG (mg/dL)'])

        # 2. Compare bolus BG to BG 3 hours later
        compareValues = {}
        for _, bolus in insulin.iterrows():
            food_bolus = bolus['InsulinDelivered']
            bolus_time = bolus['CompletionDateTime']
            bolus_bg = bolus['BG (mg/dL)']

            if food_bolus != 0.0 and not pd.isna(bolus_bg):
                # Find BG reading 3 hours after bolus time
                bg_2hr = None
                bg_after_2hr = bg[(bg['EventDateTime'] >= bolus_time + timedelta(hours=3))]

                if not bg_after_2hr.empty:
                    bg_2hr = bg_after_2hr.iloc[0]['Readings (mg/dL)']

                if bg_2hr is not None:
                    compareValues[bolus_bg] = bg_2hr

        # 3. Count Tallies
        high_tally = 0
        low_tally = 0
        for bolus_bg, bg_2hr in compareValues.items():
        # based off ranges recommended for type one diabetics 3 hours after eating (ADA guidelines)
            if bg_2hr > 180:  # High tally
                high_tally += 1
            elif bg_2hr < 90:  # Low tally
                low_tally += 1

        #print(compareValues) # debugger statement

        # 4. Adjust Carb Ratio
        if (high_tally -3)> low_tally: # -1 because we don't want to make changes because of just 1 instance
            return "Decrease carb ratio value by 1 (more insulin)"
        elif (low_tally -1) > high_tally:
            return "Increase carb ratio value by 1 (less insulin)"
        else:
            return "No changes needed"
        

    # helper function for carb ratio to determine if time2 is 2 hours after time1
    def isTwoHoursLater(time1, time2):
            fmt = "%Y-%m-%dT%H:%M:%S"
            time1 = datetime.strptime(time1, fmt)
            time2 = datetime.strptime(time2, fmt)

            return time1 + timedelta(hours=2) <= time2
    
    def Summary(self, specific_date, time_frame):
        output = []
        output.append(f"\nBlood Glucose and Insulin Analysis for {specific_date}")

        # mean
        BGmean = self.calcBGmean(specific_date, time_frame)
        BGmean = str(round(BGmean, 1))
        output.append(f"\nMean blood glucose value: {BGmean}")

        # median
        BGmedian = self.calcBGmedian(specific_date, time_frame)
        output.append(f"\nMedian blood glucose value: {BGmedian}")

        # time in range
        bg_TIR = self.BGtimeInRange(specific_date, time_frame)
        bg_TIR = str(round(bg_TIR, 1))
        output.append(f"\nTIR: {bg_TIR}%")

        # percent high
        percent_high = self.BGpercentHigh(specific_date, time_frame)
        percent_high = str(round(percent_high, 1))
        output.append(f"\nPercent high: {percent_high}%")

        # percent low
        percent_low = self.BGpercentLow(specific_date, time_frame)
        percent_low = str(round(percent_low, 1))
        output.append(f"\nPercent low: {percent_low}%")

        calcedNighttimeBasal = self.checkNighttimeBasal(specific_date)
        morningSpike = self.checkDawnPhenonmenon(specific_date)
        carbRatioAdjustments = self.checkCarbRatio(specific_date)

        output.append(f"\nCalculated nighttime basal: {calcedNighttimeBasal}")
        output.append(f"\nCalculated daytime basal: {morningSpike}")
        output.append(f"\nCarb Ratio Adjustments: {carbRatioAdjustments}")

        return "\n".join(output)



data_analyzer = DataAnalyzer()

summary = data_analyzer.Summary('2024-11-10', '1 day')


