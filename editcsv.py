# Open the file in read mode to load content
with open('/Users/aft/VisualStudioCodeWorkspace/Python/hmc_project/BGDataNov14.csv', 'r') as file:
    lines = file.readlines()

# Remove trailing commas from each line
cleaned_lines = [line.rstrip(',\n') + '\n' for line in lines]

# Write the cleaned lines back to the file
with open('newBG.csv', 'w') as cleaned_file:
    cleaned_file.writelines(cleaned_lines)

print("Trailing commas removed and saved to 'newBG.csv'.")
