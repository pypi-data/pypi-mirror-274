import csv
import sys
from datetime import datetime

from .config import CONFIG
from .utils import find_min_date


def record_advancement_line(target, line):
    """records the advancement information to the target rank, badge, award, or adventure"""
    target["Date"] = find_min_date(
        line
    )  # find earliest date, which will usually be the date signed off, rather than approved or recorded

    target["Version"] = line["Version"]
    target["Date Completed"] = (
        datetime.strptime(line["Date Completed"], "%m/%d/%Y").date()
        if line["Date Completed"]
        else None
    )
    target["Approved"] = bool(line["Approved"])
    target["Awarded"] = bool(line["Awarded"])
    target["MarkedCompletedBy"] = line["MarkedCompletedBy"]
    target["MarkedCompletedDate"] = (
        datetime.strptime(line["MarkedCompletedDate"], "%m/%d/%Y").date()
        if line["MarkedCompletedDate"]
        else None
    )
    target["CounselorApprovedBy"] = line["CounselorApprovedBy"]
    target["CounselorApprovedDate"] = (
        datetime.strptime(line["CounselorApprovedDate"], "%m/%d/%Y").date()
        if line["CounselorApprovedDate"]
        else None
    )
    target["LeaderApprovedBy"] = line["LeaderApprovedBy"]

    # Scoutbook export for merit badges has the leaderapprovedby and leaderapproveddate columns reversed, so we reverse them
    try:
        target["LeaderApprovedDate"] = (
            datetime.strptime(line["LeaderApprovedDate"], "%m/%d/%Y").date()
            if line["LeaderApprovedDate"]
            else None
        )
    except ValueError:
        target["LeaderApprovedDate"] = (
            datetime.strptime(line["LeaderApprovedBy"], "%m/%d/%Y").date()
            if line["LeaderApprovedBy"]
            else None
        )
        target["LeaderApprovedBy"] = line["LeaderApprovedDate"]

    target["AwardedBy"] = line["AwardedBy"]
    target["AwardedDate"] = (
        datetime.strptime(line["AwardedDate"], "%m/%d/%Y").date()
        if line["AwardedDate"]
        else None
    )


def record_whole_award(scout, award_type, line):
    award_type = " ".join(award_type)  # joins "Merit", "Badge" into "Merit Badge"

    if (
        line["Advancement"].split()[-1] == "Scout"
        and len(line["Advancement"].split()) == 2
    ):
        rank = line["Advancement"].split()[0]  # takes "Eagle Scout" and makes "Eagle"
    else:
        rank = " ".join((word for word in line["Advancement"].split()))

    if rank in CONFIG.get("cub_scout_ranks"):
        award_type = "Cub Scout Rank"

    if f"{award_type}s" not in scout:
        scout[f"{award_type}s"] = {}  # "Adventures", "Merit Badges", "Ranks", etc.

    scout[f"{award_type}s"][rank] = {}  # "Ranks"."Eagle"."Date"
    record_advancement_line(scout[f"{award_type}s"][rank], line)


def record_rank_requirement(scout, award_type, line):
    """records a rank requirement for a scout
    award_type will normally be something like ("Eagle", "Scout", "Rank", "Requirement")
    """
    if " ".join(award_type[:-2]) in CONFIG.get("cub_scout_ranks"):
        destination = "Cub Scout Ranks"
    else:
        destination = "Ranks"

    if destination not in scout:
        scout[destination] = {}
    rank = " ".join(
        [
            word
            for word in award_type[0:-2]
            if len(award_type[0:-2]) == 1
            or (len(award_type[0:-2]) > 1 and word != "Scout")
        ]
    )  # joins "Eagle Scout Rank Requirement into "Eagle" by ignoring the word "Scout" in "Life Scout" or "Star Scout". Also joins First Class Rank Requirement into "First Class"
    requirement = line["Advancement"].replace("#", "")
    if rank not in scout[destination]:
        scout[destination][rank] = {}
    if "Requirements" not in scout[destination][rank]:
        scout[destination][rank]["Requirements"] = {}
    scout[destination][rank]["Requirements"][requirement] = {}
    record_advancement_line(scout[destination][rank]["Requirements"][requirement], line)


def record_award_requirement(scout, award_type, line):
    if "Adventure" in award_type:
        award_type = " ".join(award_type[-2:])
    else:
        award_type = " ".join(award_type)
    if f"{award_type}s" not in scout:
        scout[f"{award_type}s"] = {}
    if "#" in line["Advancement"]:
        award = " ".join(line["Advancement"].split()[0:-1])
        requirement = line["Advancement"].split()[-1].replace("#", "")
    else:
        award = line["Advancement"]
        requirement = line["Advancement"]
    if award not in scout[f"{award_type}s"]:
        scout[f"{award_type}s"][award] = {}
    scout[f"{award_type}s"][award][requirement] = {}
    record_advancement_line(scout[f"{award_type}s"][award][requirement], line)


def process_line(scouts, line):
    name = f"{line['Last Name']}, {line['First Name']}"
    if name not in scouts:
        print(
            f"{line['Last Name']}, {line['First Name']} not found in personal data file",
            file=sys.stderr,
        )
    scouts[name] = {
        "Data": {
            "BSA Member ID": line["BSA Member ID"],
            "First Name": line["First Name"],
            "Last Name": line["Last Name"],
        }
    }
    scout = scouts[name]

    match line["Advancement Type"].strip().split():
        case (
            ("Rank",)
            | ("Adventure",)
            | ("Award",)
            | (
                "Merit",
                "Badge",
            ) as award_type
        ):
            record_whole_award(scout, award_type, line)

        case (*_, "Rank", "Requirement") as award_type:
            record_rank_requirement(scout, award_type, line)

        case (
            (
                ("Webelos" | "Wolf" | "Bear" | "Tiger" | "Lion"),
                "Adventure",
                "Requirement",
            )
            | ("Adventure", "Requirement")
            | ("Award", "Requirement")
            | (
                "Merit",
                "Badge",
                "Requirement",
            ) as award_type
        ):
            record_award_requirement(scout, award_type, line)

        case _:
            pass


def record_advancement(advancement, scouts):
    if not scouts:
        scouts = {}
    try:
        with open(advancement, "r") as f:
            reader = csv.DictReader(f)
            for line in reader:
                process_line(scouts, line)
    except TypeError:
        reader = csv.DictReader(advancement)
        for line in reader:
            process_line(scouts, line)
    return scouts
