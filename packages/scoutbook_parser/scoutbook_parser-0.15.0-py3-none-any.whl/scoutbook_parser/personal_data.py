import csv
import sys
from datetime import datetime


def read_personal_scout(line):
    """takes the fields from the personal_data.csv file and puts them into a dictionary, verifying dates and other information"""
    name = f"{line['Last Name']}, {line['First Name']}"
    return {
        name: {
            "Data": {
                "User ID": line["UserID"],
                "BSA ID": line["BSA Member ID"],
                "First Name": line["First Name"],
                "Suffix": line["Suffix"],
                "Last Name": line["Last Name"],
                "Nickname": line["Nickname"],
                "Address 1": line["Address 1"],
                "Address 2": line["Address 2"],
                "City": line["City"],
                "State": line["State"],
                "Zip": line["Zip"],
                "Home Phone": line["Home Phone"],
                "School Grade": line["School Grade"],
                "School Name": line["School Name"],
                "LDS": line["LDS"],
                "Swimming Classification": line["Swimming Classification"],
                "Swimming Classification Date": (
                    datetime.strptime(
                        line["Swimming Classification Date"], "%m/%d/%Y"
                    ).date()
                    if line["Swimming Classification Date"]
                    else None
                ),
                "Unit Number": line["Unit Number"],
                "Unit Type": line["Unit Type"],
                "Date Joined Scouts BSA": (
                    datetime.strptime(line["Date Joined Scouts BSA"], "%Y-%m-%d").date()
                    if line["Date Joined Scouts BSA"]
                    else None
                ),
                "Den Type": line["Den Type"],
                "Den Number": line["Den Number"],
                "Date Joined Den": (
                    datetime.strptime(line["Date Joined Den"], "%Y-%m-%d").date()
                    if line["Date Joined Den"]
                    else None
                ),
                "Patrol Name": line["Patrol Name"],
                "Date Joined Patrol": (
                    datetime.strptime(line["Date Joined Patrol"], "%Y-%m-%d").date()
                    if line["Date Joined Patrol"]
                    else None
                ),
                "Parent 1 Email": line["Parent 1 Email"],
                "Parent 2 Email": line["Parent 2 Email"],
                "Parent 3 Email": line["Parent 3 Email"],
            },
            "OA": {
                "OA Member Number": line["OA Member Number"],
                "OA Election Date": (
                    datetime.strptime(line["OA Election Date"], "%Y-%m-%d").date()
                    if line["OA Election Date"]
                    else None
                ),
                "OA Ordeal Date": (
                    datetime.strptime(line["OA Ordeal Date"], "%Y-%m-%d").date()
                    if line["OA Ordeal Date"]
                    else None
                ),
                "OA Brotherhood Date": (
                    datetime.strptime(line["OA Brotherhood Date"], "%Y-%m-%d").date()
                    if line["OA Brotherhood Date"]
                    else None
                ),
                "OA Vigil Date": (
                    datetime.strptime(line["OA Vigil Date"], "%Y-%m-%d").date()
                    if line["OA Vigil Date"]
                    else None
                ),
                "OA Active": line["OA Active"],
            },
        }
    }


def read_personal(personal):
    """takes a filename that is a personal_data.csv file and builds the scouts dictionary
    with the personal information for each scout"""
    scouts = {}

    try:
        with open(personal, "r") as f:
            reader = csv.DictReader(f)
            for line in reader:
                scouts.update(read_personal_scout(line))
    except TypeError:
        reader = csv.DictReader(personal)
        for line in reader:
            scouts.update(read_personal_scout(line))
    return scouts
