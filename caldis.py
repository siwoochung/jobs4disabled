import os
from datetime import datetime
from naver_distance import calculate_distance
import pandas as pd
# Specify the directory path
directory_path = 'users/'

# Get the current date
current_date = datetime.now().date()


directories_today = []
for entry in os.scandir(directory_path):
    if entry.is_dir() and entry.stat().st_ctime.date() == current_date:
        directories_today.append(entry.name)

print("Directories created today:")
for directory in directories_today:
    username = directory
    df = pd.read_csv("data/temp_data.csv")
    df["time"] = df["사업장 주소"].apply(calculate_distance, args=(address,))
    path = os.path.join("users/", username )
    df.to_csv(path+"/time.csv")

