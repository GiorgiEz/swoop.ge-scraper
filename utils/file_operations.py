import csv


def write_to_csv(data, path_to_csv, headers):
    with open(path_to_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
        print(f"✅ Data written to {path_to_csv}")
