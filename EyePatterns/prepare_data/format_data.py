import numpy as np


# collecting all csv files from forwarded directory
def collect_csv_data_collection_from_directory(path):
    import pandas as pd
    import os

    data_collection = []
    for csv_name in os.listdir(path):
        csv_path = os.path.join(path, csv_name)
        data_collection.append(pd.read_csv(csv_path))
    return data_collection


# filtering collected data
def filter_collected_data(data_collection):
    filtered_important_data_collection = []
    for data in data_collection:
        # collecting only important rows (time and AOI labels)
        important_data = data[['TIME', 'AOI']].values
        important_data_without_nan = clear_nan_values(important_data)

        first_time_concatenated_data = concatenate_rows_with_same_successive_aoi(important_data_without_nan)
        # second concatenating needs to be done because as result of first time concatenating (which removes rows with
        # less than 200 ms time spent on aoi field) can cause another successive repetition of rows with same aoi
        second_time_concatenated_data = concatenate_rows_adding_time_with_same_successive_aoi(
            first_time_concatenated_data)

        filtered_important_data_collection.append(second_time_concatenated_data)
    return filtered_important_data_collection


# clearing NaN values from the begin and the end of data sequence
def clear_nan_values(data):
    # clearing Nan values from front of the data sequence
    found_first_aoi = False
    data_cleared_from_front = []
    for row in data:
        if isinstance(row[1], float):
            if found_first_aoi:
                data_cleared_from_front.append(([row[0], "prazno"]))
        else:
            found_first_aoi = True
            data_cleared_from_front.append(([row[0], row[1]]))

    # clearing NaN values from the end of the sequence
    found_last_aoi = False
    reversed_cleared_data = []
    for i in range(len(data_cleared_from_front) - 1, 0, -1):
        if isinstance(data_cleared_from_front[i][1], float):
            if found_last_aoi:
                reversed_cleared_data.append(([data_cleared_from_front[i][0], data_cleared_from_front[i][1]]))
        else:
            found_last_aoi = True
            reversed_cleared_data.append(([data_cleared_from_front[i][0], data_cleared_from_front[i][1]]))

    cleared_data = list(reversed(reversed_cleared_data))
    return cleared_data


# concatenating time spent on successive AOI fields in data sequence and removing ones with time spent less than 200ms
def concatenate_rows_with_same_successive_aoi(data):
    import numpy as np

    concatenated_data = []
    current_aoi = ''
    aoi_first_time_seen = 0.0

    for row in data:
        if current_aoi == row[1]:
            continue
        else:
            # Clearing rows which have time spent on less than 200ms
            if row[0] - aoi_first_time_seen > 0.20:
                concatenated_data.append([row[0] - aoi_first_time_seen, current_aoi])
            current_aoi = row[1]
            aoi_first_time_seen = row[0]

    # last AOI that is left to append to sequence
    concatenated_data.append([data[len(data) - 1][0] - aoi_first_time_seen, current_aoi])
    return concatenated_data


# concatenating time spent on successive AOI fields (based on adding time between them, not calculating time spent)
# in data sequence
def concatenate_rows_adding_time_with_same_successive_aoi(data):
    import numpy as np

    concatenated_data = []
    current_aoi = ''
    time_spent_on_aoi = 0.0

    for row in data:
        if current_aoi == row[1]:
            time_spent_on_aoi += row[0]
            continue
        else:
            concatenated_data.append([time_spent_on_aoi, current_aoi])
            current_aoi = row[1]
            time_spent_on_aoi = row[0]

    # last AOI that is left to append to sequence
    concatenated_data.append([time_spent_on_aoi, current_aoi])
    concatenated_data = np.array(concatenated_data)
    return concatenated_data


# saving csv files into forwarded path
def save_data_as_csv(data, path):
    import csv
    import os

    filename = os.path.join(path + ".csv")
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)


# MAIN
collected_data = collect_csv_data_collection_from_directory("/home/sale/PycharmProjects/untitled/Collected_data")
filtered_data = filter_collected_data(collected_data)

for i in range(0, len(filtered_data)):
    save_data_as_csv(filtered_data[i],
                     "/home/sale/PycharmProjects/untitled/Filtered_colected_data/" + str(i))
