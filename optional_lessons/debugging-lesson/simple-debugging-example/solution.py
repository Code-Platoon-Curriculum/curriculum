import csv, traceback
animal_type = input("cats or dogs?\n")

try:
    data = open(f'./data/{animal_type}.csv')
    reader = csv.DictReader(data, skipinitialspace=True)
    for row in reader:
        print(f"{row['name']} is a {row['age']} year old {row['breed']}.")
    data.close()

except Exception:
    traceback.print_exc()
    # print(f"Sorry, we don't have any {animal_type} here.")


