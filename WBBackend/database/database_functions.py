import pandas as pd
import ./components/form.js

tripdetails = ["first_name", "last_name", "username", "password", "email", "rating", "starting_location"]

# write new trip data into table
def write_new():
  df = pd.read_csv('csvfilepath')

  # how to store info fromtheform into somearray

  # second dataframe for new row
  df_new = pd.DataFrame(data=somearray, columns=tripdetails)

  # add new row to original data
  df.append(df_new)

  # update csv file
  trips_df.to_csv

  return

# read row at index
def read(index):
  df = pd.read_csv('csvfilepath')

  # store in multiple variables?
  # photofile = df.loc[index, 'Photofile']
  # ...

  # store in one dataframe
  df_read = pd.DataFrame(data=df.loc([index], columns=tripdetails)
