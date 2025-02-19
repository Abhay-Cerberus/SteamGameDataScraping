# SteamGameDataScraping
This is a repo where the scraped data from steam api and gamalytics api (for sales estimate) is stored
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
<br>

## INSTRUCTIONS ON GETTING THE DATA YOURSELF
---------------------------------------------------------------------------------------------------------
<br>

### STEP 1 :  Run AllGames.py Script
- This will give you the csv with all the appids be it for games, dlcs, soundtracks, demos, server
- You will get all the data in a file named AllGames.csv
<p>Command for Running this</p>

```
python AllGames.py
```
#### Time it will take to complete :
- It will just take a couple of minutes
___________________________________________________________________________________________________________________
<br>

### STEP 2 : Run GameDataScraper.py Script
- It will ask you to enter the file name so you will just have to enter "AllGames"
- it will add .csv extension by itself
- The data will be saved in 3 seprate files namely base_games.csv, dlcs.csv, demos.csv
  > **_base_games.csv_ will save data for base games like their** appid, name, platforms, features, genres, total achievements, release date 
  >
  > **_dlcs.csv_ will save data for dlcs like thier** base game's appid, thier appid, name
  > 
  > **_demos.csv_ will save data for demos like thier** base game's appid, thier appid, name
<p>Command for Running this :</p>

```
python GameDataScraper.py
```
<p>After Pressing Enter paste this :</p>

```
AllGames
```

#### Time it will take to complete :
- it will take more time combined than other Scripts, its speed also depends on Write Speeds of your drive as well as how stable your network is
- For me it took around 3 to 4 days to completely extract the data (because my system and internet isn't the best)

<br>

#### <b>IMPORTANT : </b> 
- if there are network issues for you then worry not, the script will save all the errored appids for you to go through again
- if the script stops running then you still dont need to worry, it has saved a file named processed_appids so you can see which appid it has successfully gone through so you can remove them from AllGames.csv and run the script again
________________________________________________________________________________________________________________________________________
<br>

### STEP 3 : Run SaleData.py Script
- After running this you will get around 95,000 entries of sales data
- You will get all the data in a csv file named gamalytic_steam_games.csv
<p>Command for Running this :</p>

```
python SaleData.py
```
#### Time it will take to complete :
- It is relatively fast, will be done in a couple of minutes
_________________________________________________________________________________________________________________________
<br>

#### MISC STEP :
- if you have any Duplicate data in any of your Csv files you can run DropDupes.py Script
- it will take time based on your hardware
- it will still run even if the ram in your system is miniscule
- it will promt you to enter the file name 
<p>Command for Running this :</p>

```
python DropDupes.py
```
