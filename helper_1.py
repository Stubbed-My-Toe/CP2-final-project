import csv, os


HEADERS = [
    "username", "password", "cash",
    "times_played_blackjack", "times_played_dice",
    "times_played_plinko", "times_played_slots", "times_played_mines"
]




class csv_file:
    def __init__(self, path_to_csv):
        self.path_to_csv = path_to_csv
        self.headers = list(HEADERS)
        self.rows    = []
        # Create the file with headers if it doesn't exist yet
        if not os.path.exists(path_to_csv):
            with open(path_to_csv, mode="w", newline="") as f:
                csv.writer(f).writerow(HEADERS)
        self.sync()


    def sync(self):
        try:
            with open(self.path_to_csv, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                self.headers = list(reader.fieldnames) if reader.fieldnames else list(HEADERS)
                self.rows    = list(reader)
        except Exception as e:
            print(f"sync error: {e}")
            self.headers = list(HEADERS)
            self.rows    = []


    def __getitem__(self, index): return self.rows[index]
    def __len__(self): return len(self.headers)
    def __iter__(self): return iter(self.rows)
    def __str__(self):
        return "\n".join(",".join(f"{k}:{v}" for k, v in r.items()) for r in self.rows)


    def return_list_of_dict(self): return self.rows


    def add(self, content):
        if len(content) != len(self.headers):
            raise IndexError(f"len mismatch")
        try:
            with open(self.path_to_csv, mode="a", newline='\n') as file:
                csv.writer(file).writerow(content)
        except Exception as e:
            print(f"Add error: {e}")
        self.sync()


    def __delitem__(self, line):
        arow = []
        with open(self.path_to_csv, "r") as src:
            arow = list(csv.reader(src))
        if 0 <= line < len(self.rows):
            del arow[line + 1]
        try:
            with open(self.path_to_csv, "w", newline='\n') as file:
                csv.writer(file).writerows(arow)
        except Exception as e:
            print(f"Del error: {e}")
        self.sync()


    def update_row(self, checkers, new_data):
        for row in self.rows:
            if all(row.get(k) == str(v) for k, v in checkers.items()):
                row.update({k: str(v) for k, v in new_data.items()})
                break
        try:
            with open(self.path_to_csv, mode="w", newline='\n') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(self.rows)
            self.sync()
        except Exception as e:
            print(f"Update failed: {e}")




def csv_get_data(csv_f: csv_file, checkers):
    for x in csv_f:
        if all(x.get(y) == z for y, z in checkers.items()):
            return x
    return None




def csv_add_user(csv_f: csv_file, username, password, cash=1000):
    """Register a new user; returns False if username already taken."""
    for row in csv_f:
        if row.get("username") == username:
            return False
    csv_f.add([username, password, str(cash), "0", "0", "0", "0", "0"])
    return True
