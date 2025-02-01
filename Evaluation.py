from sklearn.metrics import cohen_kappa_score

ariya = [4,5,5,5,4,4,5,5,5,5,4,5,4,5,5,5,5,4,5,5,5,5,5,5,4,5,4,5,5,5,5,5]
anna =  [4,5,5,5,5,5,5,5,5,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]


score = cohen_kappa_score(ariya, anna, weights="quadratic")

print(score)