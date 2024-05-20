from .advancement import record_advancement
from .personal_data import read_personal
from .utils import DateTimeEncoder


class Parser:
    def __init__(
        self,
        personal=None,
        advancement=None,
        outfile="output",
        file_format="yaml",
        cub_scouts=False,
    ):
        if personal:
            scouts = read_personal(personal=personal)
            self.scouts = record_advancement(
                advancement=advancement, scouts=scouts
            )
        else:
            self.scouts = record_advancement(
                advancement=advancement, scouts=None
            )
        self.outfile = outfile
        self.file_format = file_format

    def dump(self):
        match self.file_format:
            case "yaml":
                import yaml

                with open(self.outfile, "w") as f:
                    yaml.safe_dump(self.scouts, f)
            case "toml":
                import toml

                with open(self.outfile, "w") as f:
                    toml.dump(self.scouts, f)
            case "json":
                import json

                with open(self.outfile, "w") as f:
                    json.dump(self.scouts, f, cls=DateTimeEncoder)

    def dumps(self):
        match self.file_format:
            case "yaml":
                import yaml

                output_func = yaml.safe_dump
            case "toml":
                import toml

                output_func = toml.dumps
            case "json":
                import json

                return json.dumps(self.scouts, cls=DateTimeEncoder)

        return output_func(self.scouts)


if __name__ == "__main__":
    parser = Parser(
        input_personal="Output_personal_data.csv",
        input_advancement="Output_advancement_data.csv",
        outfile="Output_scouts.yaml",
        file_format="yaml",
    )

    print(parser.dumps())
