import click
from objexplore import explore as explore_obj

from scoutbook_parser.parser import Parser


@click.command()
@click.option(
    "-t",
    "--output-type",
    default="yaml",
    help="output type, options are yaml (default), toml, and json",
)
@click.option(
    "-o",
    "--outfile",
    type=click.Path(dir_okay=False, writable=True),
    help='output filename, default is "output" with the extension',
)
@click.option(
    "-p",
    "--input_personal",
    type=click.Path(exists=True, dir_okay=False),
    help="input filename for personal data (optional)",
)
@click.option("-e", "--explore", is_flag=True)
@click.argument(
    "input_advancement",
    type=click.Path(exists=True, dir_okay=False),
)
def main(
    output_type=None,
    outfile=None,
    input_personal=None,
    input_advancement=None,
    explore=False,
):
    if outfile and outfile[-4:].lower() in ("json", "yaml", "toml"):
        output_type = outfile[-4:].lower()
    elif not output_type:
        output_type = "yaml"

    parser = Parser(
        input_personal=input_personal,
        input_advancement=input_advancement,
        outfile=outfile,
        file_format=output_type,
    )

    if explore:
        explore_obj(parser.scouts)
    elif outfile:
        parser.dump()
    else:
        print(parser.dumps())


if __name__ == "__main__":
    main()
