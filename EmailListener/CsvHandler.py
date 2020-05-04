import csv
import sys

sys.path.append('../')
import config


class CsvHandler():

    def __init__(self):
        self._file_name = config.csv_file_name
        self._data_read_from_csv = []
        self._csv_structure_dict = {}

    def _build_csv_structure_dict(self, columns):
        for c in columns:
            self._csv_structure_dict[c] = ''

    def _append_to_data_read_from_csv(self, row):
        keys = self._csv_structure_dict.keys()
        current_row_dict = {}
        count = 0
        for k in keys:
            current_row_dict[k] = row[count]
            count += 1
        self._data_read_from_csv.append(current_row_dict)

    def read_csv_file(self):
        # go to project directory and find persistent data folder
        with open(sys.path[1] + '\\PersistentData\\' + self._file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            got_column_names = False
            for row in csv_reader:
                if not got_column_names:
                    self._build_csv_structure_dict(row)
                    got_column_names = True
                else:
                    self._append_to_data_read_from_csv(row)

    def write_to_csv_file(self, dict_of_new_entry):
        current_list_of_entries = self._data_read_from_csv
        current_list_of_entries.append(dict_of_new_entry)
        with open(sys.path[1] + '\\PersistentData\\' + self._file_name, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=dict_of_new_entry.keys(), lineterminator='\n')
            writer.writeheader()
            for c in current_list_of_entries:
                writer.writerow(c)
            self._data_read_from_csv = current_list_of_entries

    def get_csv_structure_dict(self):
        return self._csv_structure_dict

    def get_data_read_from_csv(self):
        return self._data_read_from_csv


if __name__ == '__main__':
    csv_handler = CsvHandler()
    csv_handler.read_csv_file()
