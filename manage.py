#!/usr/bin/env python3
import os
import subprocess

import click

from app.factory import create_app, db


def start_db():
    app = create_app()
    app.app_context().push()
    db.drop_all()
    db.create_all()
    print("Database started successfully.")


operations = {"start_db": start_db}


@click.command()
@click.argument("option", type=click.Choice(list(operations.keys())))
def manage(option):
    operations[option]()


if __name__ == "__main__":
    manage()
