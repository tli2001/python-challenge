import os
import csv
from collections import Counter

#analyze records:
#total number of votes in dataset
#complete list of candidates who received votes
#percentage of votes each candidate won
#winner of the election based on popular vote

#prompt name of file
print("Choose either election_data_1 or election_data_2") #reminder of test file names
#fname = "election_data_1" #used during testing only
#fname = "election_data_2" #used during testing only

fname = input("Enter name of file in raw_data folder to analyze: ")

#input file path
fpath = os.path.join("raw_data", fname + '.csv')

#check if input file exists in directory
if (os.path.isfile(fpath)) == False:
    print("file '" + str(fpath) + "' not found! Exiting script.")
    exit()
#print("passed file verification") #used during testing

#output file path
fout = os.path.join("output", "results_" + fname + '.txt')

#summary variables
countvotes = 0 #record counter = number of votes
tallylist = [] #list to append candidates to
clist = [] #list of unique candidates
clistct = [] #list of candidate votes
clistpct = [] #list of candidate percentages

#read file [columns: Voter ID, County, Candidate]
with open(fpath, 'r') as f_in: 
    electionread = csv.reader(f_in)
    next(electionread, None)

#    s = set(electionread['Candidate'])    
    for record in electionread:
        tallylist.append(record[2])
        countvotes += 1

#print(countvotes)
c = Counter(tallylist)
clist = list(c.keys())
clistct = list(c.values())
#print(clist[0])
#print(clistct[0])

l = range(len(clistct))

for i in l:
    percentcalc = round(((clistct[i])/countvotes)*100,2)
    clistpct.append(percentcalc)
    #print(clistpct[i])

#summary analysis of records in file
m = max(clistct)
idx_of_m = clistct.index(m)
winner = (clist[idx_of_m])

#print analysis summary to terminal
print("\nElection Results\n" + "-"*40 + "\nTotal Votes: " + str(countvotes) + "\n" + "-"*40)
for i in l: 
    print(str(clist[i]) + ": " + str(clistpct[i]) + "% (" + str(clistct[i]) + ")")
print("-"*40 + "\nWinner: " + winner + "\n" + "-"*40)

#export results into a text file
with open(fout, 'w') as f_out:
    f_out.write("Election Results\n" + "-"*40 + "\nTotal Votes: " + str(countvotes) + "\n" + "-"*40 + "\n")
    for i in l: 
        f_out.write(str(clist[i]) + ": " + str(clistpct[i]) + "% (" + str(clistct[i]) + ")\n")
    f_out.write("-"*40 + "\nWinner: " + winner +"\n" + "-"*40)
