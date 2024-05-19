# UTIA Mint

## About

Utility to help UT Extension agents think about how they might model DOI minting for their projects.

## Installation

Easiest way to install is to use `pipx`:

```shell
pipx install utia_mint
```

If not, you can install with `pip`:

```shell

pip install utia_mint
```

## Usage

To use, download a CSV file that follows the UTIA model and run

```shell
mintdoi batch -c example.csv -o doibatch.xml
```

For more information, run

```shell
mintdoi --help
```
