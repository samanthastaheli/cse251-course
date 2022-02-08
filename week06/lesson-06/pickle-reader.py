import pickle

with open('grades.dat', 'rb') as f:
    mydict = pickle.load(f)
    
print(mydict)
