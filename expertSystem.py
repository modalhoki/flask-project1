# inserting data
import pandas as pd

df = pd.read_csv("db.csv", header=0)
data_testing = df["input"]
data_type = df["type"]

# set temp memory
history_data = []
diagnose_data = []
evident_data = []
intolerant_data = []
unmarked_data = []

# raw data sorting into temp memory
for i in range(len(data_testing)):
    current_type = data_type[i]
    if current_type == "History":
        history_data.append(data_testing[i])
    elif current_type == "diagnose":
        diagnose_data.append(data_testing[i])
    elif current_type == "evident":
        evident_data.append(data_testing[i])
    elif current_type == "intolereant":
        intolerant_data.append(data_testing[i])
    else:
        unmarked_data.append(data_testing[i])


