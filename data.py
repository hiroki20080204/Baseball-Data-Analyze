# === data.py ===
import csv

csv_file_path = "Cushing Academy Varsity Penguins Spring 2025 Stats.csv"

# Read CSV manually
with open(csv_file_path, newline='', encoding='utf-8') as f:
    reader = list(csv.reader(f))
    header_row = reader[1]  # Actual column names
    data_rows = reader[2:]  # Player data

header = [h.strip() for h in header_row]
position = [ "Catcher", "pitcher", ["Short Stop","Pitcher"], "Catcher", ["Third Base","Pitcher"], ["Pitcher","First Base","Center Field"], "Center Field", "Left Fireld", ["Third Base","First Base","Pitcher"], ["First Base","Pitcher"],["Second Base","Third Base"], ["Second Base","First Base"], ["Rgith Field","Pitcher"], "Center Field", "Pitcher"]
# Define keys (must match fields used in your rendering fallback logic)
batting_keys = [
    "AVG", "OBP", "OPS", "SLG",
    "HR", "XBH", "2B", "RBI", "R", "SB", "SB%", "BB"
]

pitching_keys = [
    "ERA", "FIP", "SO", "K-L", "BB", "BB/INN", "IP", "WHIP", "H"
]

fielding_keys = [
    "FPCT", "PO", "E", "Assists", "A", "Errors"
]

# Column indices
first_idx = header.index("First")
last_idx = header.index("Last")
number_idx = header.index("Number")
batting_indices = {k: header.index(k) for k in batting_keys if k in header}
pitching_indices = {k: header.index(k) for k in pitching_keys if k in header}
fielding_indices = {k: header.index(k) for k in fielding_keys if k in header}

# Player dict
players_dict = {}

def safe_float(val):
    return float(val) if val.replace('.', '', 1).isdigit() else 0.0

for row in data_rows:
    if len(row) <= max(list(batting_indices.values()) + list(pitching_indices.values()) + list(fielding_indices.values())):
        continue
    first = row[first_idx].strip()
    last = row[last_idx].strip()
    number = row[number_idx].strip()
    if not first or not last:
        continue

    full_name = f"{first} {last}"
    players_dict[full_name] = {
        "School": "Cushing Academy",
        "Grade": "-",
        "Number": number,
        "Batting": {k: safe_float(row[i]) for k, i in batting_indices.items()},
        "Pitching": {k: safe_float(row[i]) for k, i in pitching_indices.items()},
        "Fielding": {k: safe_float(row[i]) for k, i in fielding_indices.items()}
    }

# Optional: debug preview
if __name__ == "__main__":
    from pprint import pprint
    pprint({k: players_dict[k] for k in list(players_dict)[:3]}, sort_dicts=False)
