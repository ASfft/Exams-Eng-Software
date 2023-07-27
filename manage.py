#!/usr/bin/env python3
import os
import subprocess

import click

from app.factory import create_app, db
from app.initialize import initialize_database


def initialize():
    initialize_database()


operations = {"initialize": initialize}


@click.command()
@click.argument("option", type=click.Choice(list(operations.keys())))
def manage(option):
    operations[option]()


if __name__ == "__main__":
    manage()
