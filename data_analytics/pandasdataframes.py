# pandas series - can define indeces of a given label, can assign any kind of label as a index (see example below)
import numpy as np
import pandas as pd

mySeries = pd.Series( data = [2,3, 4, 5], 
                    index = ['a', 'b', 'c', 'd'])

print(mySeries)

# to create a series from a dictionary:
myDict = {"x":2, "a":5, "b":4, "c": 8}
series2 = pd.Series(myDict)

print(series2)
mySeries["a"] #access item by labels, can also access by index
print(mySeries + mySeries) # doubles series values, NaN(not a number) may occur
# a DataFrame is a type of 2D table with labeled columns that hold different types of data through python implementation

my_dict = {"name" : ["Joe", "Bob", "Frans"], 
           "age" : np.array([10,15,20]),
           "weight" : (75, 123, 239),
           "height" : pd.Series([4.5, 5, 6.1],
                                index=[0, 1, 2]),
            "siblings" : 1,
            "gender" : "Male"}

df = pd.DataFrame(my_dict) # converts dictionary to a DataFrame
print(df)

my_dict2 = {"name" : ["Joe", "Bob", "Frans"], 
           "age" : np.array([10,15,20]),
           "weight" : (75, 123, 239),
           "height" : pd.Series([4.5, 5, 6.1]),
            "siblings" : 1,
            "gender" : "Male"}

df2 = pd.dataFrame(my_dict2, 
                   index = my_dict["name"])

print(df2)