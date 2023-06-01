# inserting data
import pandas as pd

df = pd.read_csv("db.csv", header=0)
data_testing = df["input"]
data_type = df["type"]

his_data = []

for i in range(len(data_testing)):
    current_type = data_type[i]
    if current_type == "History":
        his_data.append(data_testing[i])

his_data.append("done")
