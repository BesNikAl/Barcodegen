import csv


class CsvImporter:

    @staticmethod
    def import_file(file_name: str):

        records = []

        with open(file_name, "r", encoding="utf-8-sig", newline="") as file:

            sample = file.read(1024)
            file.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=";,")
                delimiter = dialect.delimiter
            except csv.Error:
                delimiter = ";"

            reader = csv.reader(file, delimiter=delimiter)

            for row in reader:

                if not row:
                    continue

                if len(row) == 1:

                    data = row[0].strip()
                    comment = ""

                else:

                    data = row[0].strip()
                    comment = row[1].strip()

                if data == "":
                    continue

                records.append({

                    "data": data,
                    "comment": comment

                })

        return records