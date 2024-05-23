import csv
import json
from datetime import date, datetime


class DateTimeEncoder(json.JSONEncoder):
    """allows json encoder to write datetime or date items as isoformat"""

    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()

        return json.JSONEncoder.default(
            self,
        )


def check_duplicate(iterable):
    """returns true if the iterable has any duplicated items"""
    return not len(set(iterable)) == len(iterable)


def find_min_date(line):
    """find the earliest date if any in a csv.dictreader line
    returns the earliest datetime object found for a key with "Date"
    or None, if no date is found"""
    my_date_min = datetime.today()
    found_date = False

    for key, value in line.items():
        if value and "Date" in key:
            try:
                my_date = datetime.strptime(value, "%m/%d/%Y")
                my_date_min = min(my_date_min, my_date)
                found_date = True
            except ValueError:
                continue
    if found_date:
        return my_date_min.date()
    else:
        print("No dates found")
        return None


def verify_personal(file):
    """returns true if all the lines represent distinct users, and all users have a
    first name, last name, unit number and at least one email"""
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        ids = [line["BSA Member ID"] for line in reader]
        f.seek(0)
        if not (
            all(
                (
                    line["First Name"],
                    line["Last Name"],
                    line["Unit Number"],
                    line["Parent 1 Email"],
                )
                for line in reader
            )
        ):
            print("some data missing")
            return False
        if check_duplicate(ids):
            print("duplicate id found")
            return False
    return True
