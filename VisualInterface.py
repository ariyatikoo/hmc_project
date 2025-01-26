import csv
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# DataLoader Class
class DataLoader:
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
        
# BGPlotter Class
class BGPlotter:
    def __init__(self, bg_data):
        self.bg_data = bg_data

    def plot_past_3_days(self):
        if self.bg_data is not None:
            try:

                self.bg_data['EventDateTime'] = pd.to_datetime(self.bg_data['EventDateTime'])
                
                self.bg_data.set_index('EventDateTime', inplace=True)

                # Plot the BG data for the past 3 days
                plt.figure(figsize=(10, 6))
                plt.plot(self.bg_data.index, self.bg_data['Glucose'], marker='o', color='pink', label='Blood Glucose')

                # Add labels and title
                plt.xlabel('Date & Time')
                plt.ylabel('Blood Glucose (mg/dL)')
                plt.title('Blood Glucose for the Past 3 Days')

                # Rotate x-axis labels for better readability
                plt.xticks(rotation=45)

                # Add a legend
                plt.legend()

                # Show the plot
                plt.tight_layout()
                plt.show()

            except Exception as e:
                print(f"Error while plotting: {e}")
        else:
            print("Error: No BG data available.")


if __name__ == "__main__":

    data_loader = DataLoader()

    bgPast3Days = data_loader.getPast3DaysBg("2024-11-18")


    if bgPast3Days is not None:
        bg_plotter = BGPlotter(bgPast3Days)
        bg_plotter.plot_past_3_days() 
    else:
        print("Error: Failed to retrieve BG data for the past 3 days.")
