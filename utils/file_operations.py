import csv

def write_to_csv(data, path_to_csv, headers):
    """ Writes data to csv file. """
    try:
        with open(path_to_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)
            print(f"✅ Data written to {path_to_csv}")
    except PermissionError:
        print(f"❌ Permission denied: Cannot write to {path_to_csv}. File might be open.")
    except FileNotFoundError:
        print(f"❌ File not found: Check if the directory exists for {path_to_csv}.")
    except IOError as e:
        print(f"❌ I/O error occurred while writing to CSV: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
