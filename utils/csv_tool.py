import csv


# 寫入 csv
def write_data_to_csv(file_name):
    with open(f"../test_data/{file_name}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        rate = 6
        for i in range(1600):
            rate = i * 0.01
            rate = "{:.2f}".format(rate)
            writer.writerow([rate])


# 讀取 csv
def read_data_from_csv(file_name):
    data = []
    with open(
        f"/Users/rowenlin/Desktop/pb-rowen/test_data/{file_name}.csv",
        newline="",
    ) as file:
        rows = csv.reader(file)
        for row in rows:
            data.append(row)
    return data


# write_data_to_csv("rate_data_set")
# read_data_from_csv("rate_data_set")
