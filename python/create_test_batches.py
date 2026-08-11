import csv
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]

source_file = project_root / "data" / "supermarket_sales_clean.csv"
incoming_dir = project_root / "data" / "incoming"

initial_file = incoming_dir / "initial_sales.csv"
new_file = incoming_dir / "new_sales.csv"


incoming_dir.mkdir(exist_ok=True)

with open(source_file, "r", encoding="utf-8", newline="") as file:
    reader = csv.reader(file)
    header = next(reader)
    rows = list(reader)


initial_rows = rows[:990]
new_rows = rows[990:]


with open(initial_file, "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(initial_rows)


with open(new_file, "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(new_rows)


print(f"Initial file: {len(initial_rows)} rows")
print(f"New file: {len(new_rows)} rows")