import click
from utia_mint.mint import XMLGenerator


@click.group()
def cli() -> None:
    pass


@cli.command("batch", help="Mint a batch of DOIs")
@click.option(
    "--csv",
    "-c",
    required=True,
    help="Path to CSV to generate XML from",
)
@click.option(
    "--output",
    "-o",
    default="output.xml",
    help="Destination path to write XML to",
)
@click.option(
    "--email",
    "-e",
    default="utiaitsdev@utk.edu",
    help="Email address of the depositor",
)
@click.option(
    "--name",
    "-n",
    default="UTIA",
    help="Name of the Depositor",
)
def get_command(
    csv: str,
    output: str,
    email: str,
    name: str,
) -> None:
    x = XMLGenerator(csv, email, name)
    x.write_xml(output)
