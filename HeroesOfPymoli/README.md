
# Unit 4 | Assignment - Pandas, Pandas, Pandas

## Background

The data dive continues!

Now, it's time to take what you've learned about Python Pandas and apply it to new situations. For this assignment, you'll need to complete **1 of 2**  Data Challenges. Once again, it's your choice which you choose. Just be sure to give it your all -- as the skills you hone will become powerful tools in your data analytics tool belt.

## Option 1: Heroes of Pymoli

Congratulations! After a lot of hard work in the data munging mines, you've landed a job as Lead Analyst for an independent gaming company. You've been assigned the task of analyzing the data for their most recent fantasy game Heroes of Pymoli. 

Like many others in its genre, the game is free-to-play, but players are encouraged to purchase optional items that enhance their playing experience. As a first task, the company would like you to generate a report that breaks down the game's purchasing data into meaningful insights.

Your final report should include each of the following:

**Player Count**
**Purchasing Analysis (Total)**
**Gender Demographics**
**Purchasing Analysis (Gender)** 
**Age Demographics**
**Top Spenders**
**Most Popular Items**
**Most Profitable Items**

As final considerations:

* Your script must work for both data-sets given.
* You must use the Pandas Library and the Jupyter Notebook.
* You must submit a link to your Jupyter Notebook with the viewable Data Frames. 
* You must include an exported markdown version of your Notebook called  `README.md` in your GitHub repository.  
* You must include a written description of three observable trends based on the data. 

## Three observable trends based on the data (purchase_data.json)

1) The most popular items are priced around $2, while the most profitable items are priced closer to $4.
2) The top three age groups [20-24, 15-19, 25-29] make up over 75% of the player base, and their spend also makes up 75% of total revenue.
3) Within the population, males spend more on average than females [$4.02 vs $3.83 normalized]


```python
import pandas as pd
import os
```


```python
# Create a reference for the input files
csv_path1 = "purchase_data.json"
csv_path2 = "purchase_data2.json"

csv_path = csv_path1 #select file to read in

# Read selected file into a Pandas DataFrame
pdata_df = pd.read_json(csv_path)

pdata_df.head() # Print the first five rows of data to the screen
pdata_df.describe() #Print statistics of the data
headers = list(pdata_df) # Place headers of dataframe into a list
headers
```




    ['Age', 'Gender', 'Item ID', 'Item Name', 'Price', 'SN']




```python
# Total Unique Player Count

#Remove duplicates by SN to get unique set of players for normalizing Gender and Age calculations
agegender_df = pdata_df.drop_duplicates(subset='SN')

player_count = pdata_df['SN'].unique().size
totalplayercount_df = pd.DataFrame({
                                    "Total Number of Players":[player_count]
                                   })
totalplayercount_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Number of Players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>573</td>
    </tr>
  </tbody>
</table>
</div>




```python
#* Number of Unique Items
item_count = pdata_df['Item ID'].unique().size
#* Average Purchase Price
avg_price = pdata_df['Price'].mean().round(2)
#* Total Number of Purchases
total_purchases = pdata_df['Item ID'].size
#* Total Revenue
total_revenue = pdata_df['Price'].sum().round(2)

#**Purchasing Analysis (Total)**
totpurchanalysis_df = pd.DataFrame({
    "Number of Unique Items": [item_count], 
    "Average Purchase Price": [avg_price], 
    "Total Number of Purchases":[total_purchases],
    "Total Revenue":[total_revenue]
})
totpurchanalysis_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Purchase Price</th>
      <th>Number of Unique Items</th>
      <th>Total Number of Purchases</th>
      <th>Total Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2.93</td>
      <td>183</td>
      <td>780</td>
      <td>2286.33</td>
    </tr>
  </tbody>
</table>
</div>




```python
#**Gender Demographics**
#* Percentage and Count of Male Players
#* Percentage and Count of Female Players
#* Percentage and Count of Other / Non-Disclosed

gender_count = agegender_df['Gender'].value_counts()
genderdemographics_df = pd.DataFrame(gender_count)
genderdemographics_df = genderdemographics_df.rename(columns={"Gender":"Total Players"})
genderdemographics_df['Percentage of Players'] = round((genderdemographics_df['Total Players']/player_count)*100,2)

genderdemographics_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Players</th>
      <th>Percentage of Players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>465</td>
      <td>81.15</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>100</td>
      <td>17.45</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>8</td>
      <td>1.40</td>
    </tr>
  </tbody>
</table>
</div>




```python
#The below each broken by gender
#gendergb_df = agegender_df[['Gender','Price']]
gender_groupby = pdata_df.groupby('Gender')
#Purchase Count
genderpurchcount = gender_groupby['SN'].count()
#Average Purchase Price
genderavgprice = gender_groupby['Price'].mean().round(2)
#Total Purchase Value
gendertotalpurch = gender_groupby['Price'].sum()
#Normalized Totals
gendernormalizedprice = round(gendertotalpurch/gender_count,2)

#Purchasing Analysis (Gender)
genderpurchanalysis_df = pd.DataFrame({
    "Purchase Count": genderpurchcount, 
    "Average Purchase Price": genderavgprice, 
    "Total Purchase Value": gendertotalpurch,
    "Normalized Totals": gendernormalizedprice
})
genderpurchanalysis_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Purchase Price</th>
      <th>Normalized Totals</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Female</th>
      <td>2.82</td>
      <td>3.83</td>
      <td>136</td>
      <td>382.91</td>
    </tr>
    <tr>
      <th>Male</th>
      <td>2.95</td>
      <td>4.02</td>
      <td>633</td>
      <td>1867.68</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>3.25</td>
      <td>4.47</td>
      <td>11</td>
      <td>35.74</td>
    </tr>
  </tbody>
</table>
</div>




```python
#check max age of dataset; default to 40 if less
binmax = (max(pdata_df['Age'].max(),40)) 
bins = [0,9,14,19,24,29,34,39,binmax]
#The below each broken into bins of 4 years (i.e. <10, 10-14, 15-19, etc.)
bin_groups = ["<10","10-14","15-19","20-24","25-29","30-34","35-39","40+"]
binmax
```




    45




```python
#apply bins to dataframe on Age Group
pdata_df["Age Group"] = pd.cut(pdata_df['Age'], bins, labels=bin_groups)

#remove duplicate SNs on dataframe with Age Group
agegender_df = pdata_df.drop_duplicates(subset='SN')

#Age Demographics
age_count = agegender_df['Age Group'].value_counts()
agedemographics_df = pd.DataFrame(age_count)
agedemographics_df = agedemographics_df.rename(columns={"Age Group":"Total Count"})
agedemographics_df['Percentage of Players'] = round((agedemographics_df['Total Count']/player_count)*100,2)
#agedemographics_df = agedemographics_df.reset_index()
agedemographics_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Count</th>
      <th>Percentage of Players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>20-24</th>
      <td>259</td>
      <td>45.20</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>100</td>
      <td>17.45</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>87</td>
      <td>15.18</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>47</td>
      <td>8.20</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>27</td>
      <td>4.71</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>23</td>
      <td>4.01</td>
    </tr>
    <tr>
      <th>&lt;10</th>
      <td>19</td>
      <td>3.32</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>11</td>
      <td>1.92</td>
    </tr>
  </tbody>
</table>
</div>




```python
age_groupby = pdata_df.groupby('Age Group')
#Purchase Count
agepurchcount = pdata_df['Age Group'].value_counts()
#Average Purchase Price
ageavgprice = age_groupby['Price'].mean().round(2)
#Total Purchase Value
agetotalpurch = age_groupby['Price'].sum().round(2)
#Normalized Totals
agenormalizedprice = round(agetotalpurch/age_count,2)

#Purchase Analysis (Age)
agepurchanalysis_df = pd.DataFrame({
    "Purchase Count": agepurchcount, 
    "Average Purchase Price": ageavgprice, 
    "Total Purchase Value": agetotalpurch,
    "Normalized Totals": agenormalizedprice
})
agepurchanalysis_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Purchase Price</th>
      <th>Normalized Totals</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>10-14</th>
      <td>2.77</td>
      <td>4.22</td>
      <td>35</td>
      <td>96.95</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>2.91</td>
      <td>3.86</td>
      <td>133</td>
      <td>386.42</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>2.91</td>
      <td>3.78</td>
      <td>336</td>
      <td>978.77</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>2.96</td>
      <td>4.26</td>
      <td>125</td>
      <td>370.33</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>3.08</td>
      <td>4.20</td>
      <td>64</td>
      <td>197.25</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>2.84</td>
      <td>4.42</td>
      <td>42</td>
      <td>119.40</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>3.16</td>
      <td>4.89</td>
      <td>17</td>
      <td>53.75</td>
    </tr>
    <tr>
      <th>&lt;10</th>
      <td>2.98</td>
      <td>4.39</td>
      <td>28</td>
      <td>83.46</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Top Spenders
spenders_df = pdata_df[['SN','Price']]
spenders_groupby = spenders_df.groupby('SN')
#Identify the the top 5 spenders in the game by total purchase value, then list (in a table):
#SN
#Purchase Count
spenderpurchcount = spenders_df['SN'].value_counts()
#Average Purchase Price
spenderavgprice = spenders_groupby['Price'].mean()
#Total Purchase Value
spendertotalpurch = spenders_groupby['Price'].sum()

#Top Spender Analysis (SN)
topspenderanalysis_df = pd.DataFrame({
    "Purchase Count": spenderpurchcount, 
    "Average Purchase Price": spenderavgprice, 
    "Total Purchase Value": spendertotalpurch
})
topspendsorted = topspenderanalysis_df.sort_values(by=['Total Purchase Value'], ascending=False)
topspendsorted.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Purchase Price</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Undirrala66</th>
      <td>3.412000</td>
      <td>5</td>
      <td>17.06</td>
    </tr>
    <tr>
      <th>Saedue76</th>
      <td>3.390000</td>
      <td>4</td>
      <td>13.56</td>
    </tr>
    <tr>
      <th>Mindimnya67</th>
      <td>3.185000</td>
      <td>4</td>
      <td>12.74</td>
    </tr>
    <tr>
      <th>Haellysu29</th>
      <td>4.243333</td>
      <td>3</td>
      <td>12.73</td>
    </tr>
    <tr>
      <th>Eoda93</th>
      <td>3.860000</td>
      <td>3</td>
      <td>11.58</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Most Popular Items
items_df = pdata_df[['Item ID', 'Item Name', 'Price']]
items_groupby = items_df.groupby('Item ID')
#Identify the 5 most popular items by purchase count, then list (in a table):
#Item ID
#Item Name
#itemname = items_df['Item Name'].unique()

#Purchase Count
itempurchcount = items_df['Item ID'].value_counts()
#Item Price
itemsunique_df = items_df.drop_duplicates(subset='Item ID')
itemprice = itemsunique_df['Price']
#itemprice.head()
#Total Purchase Value
itemtotalpurch = items_groupby['Price'].sum()
#itemtotalpurch.head()

itp_df = pd.DataFrame(itemtotalpurch)
itp_df = itp_df.rename(columns={"Price":"Total Purchase Value"})
itp_df = itp_df.reset_index()
#itp_df.head()
ipc_df = pd.DataFrame(itempurchcount)
ipc_df = ipc_df.reset_index()
ipc_df = ipc_df.rename(columns={"Item ID": "Purchase Count", "index":"Item ID"})
#ipc_df.head()
#itemsunique_df.head()

itemsuniquetp_df = pd.merge(itemsunique_df, itp_df, on="Item ID")
#itemsuniquetp_df.head()
#len(itemsuniquetp_df)

itemsanalysis_df = pd.merge(itemsuniquetp_df, ipc_df, on="Item ID")


#Most Popular Items Analysis (Item ID)
popularitemssorted = itemsanalysis_df.sort_values(by=['Purchase Count'], ascending=False)
popularitemssorted.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Item ID</th>
      <th>Item Name</th>
      <th>Price</th>
      <th>Total Purchase Value</th>
      <th>Purchase Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>53</th>
      <td>39</td>
      <td>Betrayal, Whisper of Grieving Widows</td>
      <td>2.35</td>
      <td>25.85</td>
      <td>11</td>
    </tr>
    <tr>
      <th>88</th>
      <td>84</td>
      <td>Arcane Gem</td>
      <td>2.23</td>
      <td>24.53</td>
      <td>11</td>
    </tr>
    <tr>
      <th>68</th>
      <td>175</td>
      <td>Woeful Adamantite Claymore</td>
      <td>1.24</td>
      <td>11.16</td>
      <td>9</td>
    </tr>
    <tr>
      <th>33</th>
      <td>13</td>
      <td>Serenity</td>
      <td>1.49</td>
      <td>13.41</td>
      <td>9</td>
    </tr>
    <tr>
      <th>49</th>
      <td>31</td>
      <td>Trickster</td>
      <td>2.07</td>
      <td>18.63</td>
      <td>9</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Most Profitable Items
#Identify the 5 most profitable items by total purchase value, then list (in a table):
#Item ID
#Item Name
#Purchase Count
#Item Price
#Total Purchase Value
profitableitemssorted = itemsanalysis_df.sort_values(by=['Total Purchase Value'], ascending=False)
profitableitemssorted.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Item ID</th>
      <th>Item Name</th>
      <th>Price</th>
      <th>Total Purchase Value</th>
      <th>Purchase Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>50</th>
      <td>34</td>
      <td>Retribution Axe</td>
      <td>4.14</td>
      <td>37.26</td>
      <td>9</td>
    </tr>
    <tr>
      <th>84</th>
      <td>115</td>
      <td>Spectral Diamond Doomblade</td>
      <td>4.25</td>
      <td>29.75</td>
      <td>7</td>
    </tr>
    <tr>
      <th>45</th>
      <td>32</td>
      <td>Orenmir</td>
      <td>4.95</td>
      <td>29.70</td>
      <td>6</td>
    </tr>
    <tr>
      <th>79</th>
      <td>103</td>
      <td>Singed Scalpel</td>
      <td>4.87</td>
      <td>29.22</td>
      <td>6</td>
    </tr>
    <tr>
      <th>112</th>
      <td>107</td>
      <td>Splitter, Foe Of Subtlety</td>
      <td>3.61</td>
      <td>28.88</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>


