# datadaft yt channel, playlist 'python for data analysis', video #7
# ex
myDict = {"name": "Ariya", "age": 16, "city":"Medina"}
print(myDict)
print(myDict["name"])
myDict["school"] = "Wayzata High School"
print(myDict)
del myDict["age"]
len(myDict)
"name" in myDict #for keys, not values
myDict.keys()
myDict.values() #"Medina" in __
myDict.items
myTableDict = {"name": ["Ariya", "Kitchi"], # also can be done with pandas, easier
               "age": [16, 4],
               "city": ["Medina", "Medina"]}
# sets, all values must be unique
mySet = {1,2,3,4,5}
mySet.add(8)
mySet.remove(2)
#does not support indexing !, does len, min, max, in
6 in mySet
# main use for sets is checking for duplicates:
set1 = {1,3,5,6}
set2 = {1,2,3,4}
set1.union(set2) # gets both sets combined, no overlaps
set1.intersection(set2) #gets same values, can also check set.difference, set.issubset