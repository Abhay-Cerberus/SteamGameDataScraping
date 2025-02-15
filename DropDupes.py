import dask.dataframe as dd

FILENAME = input('Enter The File Name (without .csv) : ')
FILENAME = FILENAME + ".csv"

if FILENAME=="base_games.csv":
    dtypes = {
    'achievements_total': 'object',
    'dlcs': 'object',
    'metacritic': 'object',
    'steam_appid': 'object'     
    }
elif FILENAME=="demos.csv":
    dtypes={'demo_appid': 'object',
       'full_game_appid': 'object'
       }
elif FILENAME=="dlcs.csv":
    dtypes={'dlc_appid': 'object',
       'base_appid': 'object',
       'name': 'object'
       }
elif FILENAME=="Done.csv":
    dtypes={'appid':'object'}
else:
    print("Enter a valid FileName!!")
    exit()
       
# Read the CSV file with Dask using the specified dtypes.
df = dd.read_csv(FILENAME,dtype=dtypes)

# Drop duplicates (Dask will do this in parallel)
df_unique = df.drop_duplicates()

# Write the deduplicated data to a single CSV file.
# Note: single_file=True forces the output into one file (which may be slower for huge files).
df_unique.to_csv(FILENAME, single_file=True, index=False)

print(f"Deduplication complete. Unique rows saved to {FILENAME}")
