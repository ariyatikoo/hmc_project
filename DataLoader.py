import csv
import datetime
import pandas as pd

#pd.set_option('display.max_rows', None)


class DataLoader:
    def __init__(self):
        # Initialize attributes
        self.bg = None
        self.insulin = None
        self.bgTable = None
        self.insulinTable = None


    # Create dictionaries from CSV files
    def getBGDict(self):
        with open('/Users/aft/VisualStudioCodeWorkspace/Python/hmc_project/TestBGFile.csv', 'r') as f:
            dict_reader = csv.DictReader(f)
            self.bg = {}  # Initialize bg dictionary

            for row in dict_reader:
                key = row['EventDateTime']
                if key not in self.bg:
                    self.bg[key] = []  # Initialize list for each key
                self.bg[key].append(row)  # Append row dictionary to list
            return self.bg
        
    def getInsulinDict(self):
        with open('/Users/aft/VisualStudioCodeWorkspace/Python/hmc_project/TestInsulinFile.csv', 'r') as f:
            dict_reader = csv.DictReader(f)
            self.insulin = {}  # Initialize insulin dictionary

            for row in dict_reader:
                key = row['CompletionDateTime']
                if key not in self.insulin:
                    self.insulin[key] = []  # Initialize list for each key
                self.insulin[key].append(row)  # Append row dictionary to list
            return self.insulin 

    def read_from_csv(self, filename):
        with open(filename, newline="") as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            print(header)
            for row in reader:
                print(row) 

    # Create data tables using pandas
    def getBGTable(self): 
        try:
            self.bgTable = pd.read_csv(
                '/Users/aft/VisualStudioCodeWorkspace/Python/hmc_project/TestBGFile.csv',
                #on_bad_lines='skip'
            )
            self.bgTable.set_index('EventDateTime')
            return self.bgTable
        except pd.errors.ParserError as e:
            print(f"ParserError: {e}")
            return None

    def getInsulinTable(self):  
        try:
            self.insulinTable = pd.read_csv(
                '/Users/aft/VisualStudioCodeWorkspace/Python/hmc_project/TestInsulinFile.csv',
                #on_bad_lines='skip'
            )
            self.insulinTable = self.insulinTable.set_index('CompletionDateTime')
            return self.insulinTable
        except pd.errors.ParserError as e:
            print(f"ParserError: {e}")
            return None
        
    # Filter BG data for a specific date
    def getBGforOneDay(self, specific_date):
        if self.bg is None:
            print("BG data has not been loaded.")
            return None

        try: 
            # Create DataFrame from bg dictionary
            df = pd.DataFrame(self.bg.values())
            

            df = pd.json_normalize(df[0]) 

            # Convert EventDateTime to datetime format
            df['EventDateTime'] = pd.to_datetime(df['EventDateTime'])

            # Filter rows for the specified date
            filtered_df = df[df['EventDateTime'].dt.date == datetime.datetime.strptime(specific_date, "%Y-%m-%d").date()]

            return filtered_df
        except Exception as e:
            print(f"Error: {e}")
            return None

     # Filter insulin data for a specific date
    def getInsulinforOneDay(self, specific_date):
        if self.insulin is None:
            print("Insulin data has not been loaded.")
            return None

        try: 
            # Create DataFrame from bg dictionary
            df = pd.DataFrame(self.insulin.values())
            

            df = pd.json_normalize(df[0]) 

            # Convert CompletionDateTime to datetime format
            df['CompletionDateTime'] = pd.to_datetime(df['CompletionDateTime'])

            # Filter rows for the specified date
            filtered_df = df[df['CompletionDateTime'].dt.date == datetime.datetime.strptime(specific_date, "%Y-%m-%d").date()]

            return filtered_df
        except Exception as e:
            print(f"Error: {e}")
            return None
      
    
    # get bg data for past 3 days when specifying a specific day
    def getPast3DaysBg(self, specific_date):
        if self.bg is None:
            print("BG data has not been loaded. Please call getBGDict first.")
            return None

        try:
            # Create DataFrame from bg dictionary
            df = pd.DataFrame(self.bg.values())
            

            df = pd.json_normalize(df[0]) 

            # Convert EventDateTime to datetime format
            df['EventDateTime'] = pd.to_datetime(df['EventDateTime'])


            specific_datetime = datetime.datetime.strptime(specific_date, "%Y-%m-%d").date()

            # Calculate the previous days
            days_to_filter = {specific_datetime, 
                              specific_datetime - datetime.timedelta(days=1), 
                              specific_datetime - datetime.timedelta(days=2)}

            # Filter rows for the specified dates
            bgPast3Days = df[df['EventDateTime'].dt.date.isin(days_to_filter)]

            return bgPast3Days
        

        except Exception as e:
            print(f"Error: {e}")
            return None
        
    # get insulin data for past 3 days when specifying a specific day
    def getPast3DaysInsulin(self, specific_date):
        if self.insulin is None:
            print("Insulin data has not been loaded")
            return None

        try:
            # Create DataFrame from bg dictionary
            df = pd.DataFrame(self.insulin.values())
            
            df = pd.json_normalize(df[0]) 

            # Convert CompletionDateTime to datetime format
            df['CompletionDateTime'] = pd.to_datetime(df['CompletionDateTime'])

            specific_datetime = datetime.datetime.strptime(specific_date, "%Y-%m-%d").date()

            # Calculate the previous days
            days_to_filter = {specific_datetime, 
                              specific_datetime - datetime.timedelta(days=1), 
                              specific_datetime - datetime.timedelta(days=2)}

            # Filter rows for the specified dates
            insulinPast3Days = df[df['CompletionDateTime'].dt.date.isin(days_to_filter)]

            return insulinPast3Days
        
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    


    def getNighttimeBg(self, specific_date):
        if self.bg is None:
            print("BG data has not been loaded. Please call getBGDict first.")
            return None

        try:
            self.getBGDict()
            specific_datetime = datetime.datetime.strptime(specific_date, "%Y-%m-%d")

            results = []

            for days_before in range(3):
                current_date = specific_datetime - datetime.timedelta(days=days_before)


                start_time = current_date.replace(hour=23, minute=0, second=0) - datetime.timedelta(days=1)
                end_time = current_date.replace(hour=5, minute=0, second=0)

                bg_table = self.getBGTable()

                if 'EventDateTime' in bg_table.columns:
                    bg_table['EventDateTime'] = pd.to_datetime(bg_table['EventDateTime'])
                else:
                    print("Error: 'EventDateTime' column not found in the BG table.")
                    return None

                filtered_data = bg_table[
                    (bg_table['EventDateTime'] >= start_time) &
                    (bg_table['EventDateTime'] <= end_time)
                ]

                results.append(filtered_data)

            final_results = pd.concat(results, ignore_index=True)
            return final_results

        except Exception as e:
            print(f"Error: {e}")
            return None


       
        
    def getMorningBg(self, specific_date) :
        if self.bg is None:
            print("BG data has not been loaded. Please call getBGDict first.")
            return None

        try:
           
            self.getBGDict()

            # convert data into a datetime object
            specific_datetime = datetime.datetime.strptime(specific_date, "%Y-%m-%d")

            # create list to store results for 3 days (specific_date and 2 days before)
            results = []

            #loop over the 3 days
            for days_before in range(3):
                current_date = specific_datetime - datetime.timedelta(days=days_before)

                # time range
                start_time = current_date + datetime.timedelta(hours=5)  # 5 AM
                end_time = current_date + datetime.timedelta(hours=7)  # 7 AM

  
                bg_table = self.getBGTable()

                # EventDateTime column is in datetime format
                if 'EventDateTime' in bg_table.columns:
                    bg_table['EventDateTime'] = pd.to_datetime(bg_table['EventDateTime'])
                else:
                    print("Error: 'EventDateTime' column not found in the BG table.")
                    return None

                # Filter the data within the time range
                filtered_data = bg_table[
                    (bg_table['EventDateTime'] >= start_time) &
                    (bg_table['EventDateTime'] <= end_time)
                ]

                # Append filtered data for the current day to the results list
                results.append(filtered_data)

            # Concatenate results for all 3 days into a single DataFrame
            final_results = pd.concat(results, ignore_index=True)
            return final_results

        except Exception as e:
            print(f"Error: {e}")
            return None


# Create an instance of DataLoader
data_loader = DataLoader()

# Populate dictionaries and call methods
bg = data_loader.getBGDict()
bgTable = data_loader.getBGTable()
insulin = data_loader.getInsulinDict()
insulinTable = data_loader.getInsulinTable()



print("\nBlood Glucose Data:\n")
bgOneDay = data_loader.getBGforOneDay("2025-01-01")
print(bgOneDay)

print("\nInsulin Data:\n")
insulinOneDay = data_loader.getInsulinforOneDay("2025-01-01")
print(insulinOneDay)

print("\nBlood Glucose Data for 3 Days, 2024:\n")
bgPast3Days = data_loader.getPast3DaysBg("2025-01-01")
print(bgPast3Days)

print("\nInsulin Data for 3 days:\n")
insulinPast3Days = data_loader.getPast3DaysInsulin("2025-01-01")
print(insulinPast3Days)

print("\nOvernight Blood Glucose Data:\n")
nighttimeBg = data_loader.getNighttimeBg("2025-01-01")
print(nighttimeBg)

print("\nMorning Blood Glucose Data:\n")
morningBg = data_loader.getMorningBg("2025-01-01")
print(morningBg)
