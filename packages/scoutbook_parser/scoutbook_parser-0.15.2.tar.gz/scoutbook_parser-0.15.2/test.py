from scoutbook_parser.parser import Parser
from pathlib import Path

ROOT = Path("/home/perkinsms/Projects/django-troop/django_troop/data/example_troop_scoutbook")

advancement = ROOT / "advancement.csv"
p_files = Parser(advancement=advancement)

with open(advancement, "r") as advancement_stream:
    p_streams = Parser(advancement=advancement_stream)

assert set(p_files.scouts.keys()) == set(p_streams.scouts.keys())
assert p_files.dumps() == p_streams.dumps()

personal = ROOT / "Personal_data.csv"
p_files = Parser(personal=personal, advancement=advancement)

with open(personal, "r") as personal_stream, open(advancement, "r") as advancement_stream:
    p_streams = Parser(personal=personal_stream, advancement=advancement_stream)

assert set(p_files.scouts.keys()) == set(p_streams.scouts.keys())
assert p_files.dumps() == p_streams.dumps()


with open(advancement, "r") as advancement_stream_2, open(personal, "r") as personal_stream_2:
    p_files_streams = Parser(advancement=advancement_stream_2, personal=personal)
    p_streams_files = Parser(advancement=advancement, personal=personal_stream_2)


assert set(p_files_streams.scouts.keys()) == set(p_streams_files.scouts.keys())
assert p_files_streams.dumps() == p_streams_files.dumps()
