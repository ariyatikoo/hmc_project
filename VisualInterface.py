import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
data = pd.read_csv('BGDataNov14.csv', parse_dates=['EventDateTime'])

# Extract columns
x = data['EventDateTime']  
y = data['Readings (mg/dL)']

data = data[data['Readings (mg/dL)'] > 100]
data.groupby('EventDateTime').sum()

# Create the plot
plt.figure(figsize=(8, 5))
plt.plot(x, y, marker='o', color='pink', label='Values')

# Add labels and title
plt.xlabel('Time')
plt.ylabel('BG Readings')
plt.title('BG Data Over 2 Weeks')



# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Add a legend
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()