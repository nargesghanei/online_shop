import csv


class FileHandler:
    def __init__(self, file_path='data.csv'):
        self.file_path = file_path

    def read_file(self):
        with open(self.file_path, 'r') as myfile:
            reader = csv.DictReader(myfile)
            return list(reader)

    def add_to_file(self, new_value):
        if isinstance(new_value, dict):
            fields = new_value.keys()
            new_value = [new_value]
        elif isinstance(new_value, list):
            fields = new_value[0].keys()

        with open(self.file_path, 'a') as myfile:
            writer = csv.DictWriter(myfile, fieldnames=fields)
            if myfile.tell() == 0:
                writer.writeheader()
            writer.writerows(new_value)

    def write_info_user(self, new_value):
        # check this new value is dict or list of dict
        if isinstance(new_value, dict):
            field = new_value.keys()
            new_value = [new_value]
        elif isinstance(new_value, list):
            field = new_value[0].keys()

        with open(self.file_path, 'a') as f_append:
            write = csv.DictWriter(f_append, fieldnames=field)
            # check just put header top of the file
            if f_append.tell() == 0:
                write.writeheader()
                write.writerows(new_value)
