import os
import csv

from brandon_slack.settings import FILE_NAME_CSV

class CSVFile:
    def __init__(self):
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, FILE_NAME_CSV)
        print(file_path)
        self.csv_file = open(file_path)

    def read_emails(self):
        emails = [row[0] for row in csv.reader(self.csv_file)]
        return emails

    def __del__(self):
        self.csv_file.close()

if __name__ == "__main__":
    csv_file = CSVFile()
