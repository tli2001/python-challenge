import os
import csv

#analyze records:
#total number of votes in dataset
#complete list of candidates who received votes
#percentage of votes each candidate won
#winner of the election based on popular vote


#prompt name of file
print("Choose either election_data_1 or election_data_2") #reminder of test file names
fname = "election_data_1" #used during testing only
#fname = "election_data_2" #used during testing only

#fname = input("Enter name of file in raw_data folder to analyze: ")

#input file path
fpath = os.path.join("raw_data", fname + '.csv')

#check if input file exists in directory
if (os.path.isfile(fpath)) == False:
    print("file '" + str(fpath) + "' not found! Exiting script.")
    exit()
#print("passed file verification") #used during testing

#output file path
fout = os.path.join("output", "results_" + fname + '.csv')

#summary variables
countvotes = 0 #record counter = number of votes
#revenuesum = 0 #sum of all records' revenues
priormthrev = 0 #set prior month revenue to 0

revlist = [] #list to append revenues to
revlistmth = [] #list to append month/date of revenues to
revlist.append(0) #append starting point to allow for month change calculations
revlistmth.append("") #append starting point to record correct month for change calculations
revchglist = [] #list to track monthly change in revenue
revchgmth = [] #list to track month/date of change in revenue

#read file [columns: Date and Revenue]
with open(fpath, 'r') as f_in: 
    budgetread = csv.DictReader(f_in)

#summary analysis of records in file
    for record in budgetread:
        countvotes +=1
        #revenuesum = int(record['Revenue']) + revenuesum
        revlist.append(record['Revenue'])
        revlistmth.append(record['Date'])
        revchglist.append(int(record['Revenue']) - int(priormthrev))
        revchgmth.append(record['Date'])
        priormthrev = record['Revenue']

#find max and min of monthly change in revenue, and corresponding position
    m = max(revchglist)
    n = min(revchglist)
    a = round(sum(revchglist)/len(revchglist),2)
    idx_of_m = revchglist.index(m)
    idx_of_n = revchglist.index(n)
    #print(revlist)
    #print(revchglist)
    #print(revchgmth[idx_of_m])
    #print(revchgmth[idx_of_n])

#print analysis summary to terminal
    print("\nFinancial Analysis")
    print("-"*40)
    print("Total Votes: " + str(countvotes))
    #print("Total Revenue: $" + str(revenuesum))
    print("Average Revenue Change: $" + str(a))
    print("Greatest Increase in Revenue: " + str(revchgmth[idx_of_m]) + " $" + str(m))
    print("Greatest Decrease in Revenue: " + str(revchgmth[idx_of_n]) + " $" + str(n))

#export results into a text file
with open(fout, 'w') as f_out:
    f_out.write("Financial Analysis\n")
    f_out.write("-"*40)
    f_out.write("\nTotal Votes: " + str(countvotes))
    #f_out.write("\nTotal Revenue: $" + str(revenuesum))
    f_out.write("\nAverage Revenue Change: $" + str(a))    
    f_out.write("\nGreatest Increase in Revenue: " + str(revchgmth[idx_of_m]) + " $" + str(m))
    f_out.write("\nGreatest Decrease in Revenue: " + str(revchgmth[idx_of_n]) + " $" + str(n))
