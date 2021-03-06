# collecting all csv files from forwarded directory
import os


def collect_csv_data_collection_from_directory(path):
    import pandas as pd
    import os

    data_collection = []
    for csv_name in os.listdir(path):
        csv_path = os.path.join(path, csv_name)
        data_collection.append(pd.read_csv(csv_path))
    return data_collection


# giving dictionary and sequence matrix this function returns dictionary representation (often string) of given sequence
def make_string_representation_of_sequence_matrix(dictionary, sequence_matrix, duration_threshold):
    string_representation = ""

    for row in sequence_matrix:
        if row[0] > duration_threshold:
            # just to protect myself of re editing collection document (it may contain unhealthy data xD)
            if (row[1] + 'Dugo') in dictionary:
                string_representation += dictionary[row[1] + 'Dugo']
        else:
            if (row[1] + 'Kratko') in dictionary:
                string_representation += dictionary[row[1] + 'Kratko']

    return string_representation


def format_sequences_from_student(student_name):
    collected_data = collect_csv_data_collection_from_directory("./filtered_colected_data/student_1")

    # First of all, we need to define dictionary with key-value pairs, that represents which AOI(+duration) will take letter of
    # english alphabet
    aoi_mapping_dictionary = {'pitanjeKratko': 'A', 'pitanjeDugo': 'B', 'kodKratko': 'C', 'kodDugo': 'D',
                              'odgovoriKratko': 'E', 'odgovoriDugo': 'F', 'prethodnoKratko': '',
                              'prethodnoDugo': '', 'sledeceKratko': 'G', 'sledeceDugo': 'H',
                              'praznoKratko': 'K', 'praznoDugo': 'L'}

    # This matrix is representing all string sequences of user gazes via alphabet characters
    string_sequences = []
    for data in collected_data:
        string_sequence = make_string_representation_of_sequence_matrix(aoi_mapping_dictionary, data.values, 4.5)
        if len(string_sequence)>0:
            string_sequences.append(string_sequence)

    print(string_sequences)
    return string_sequences
