import click
from click.termui import prompt

import hibterm


@click.command()
@click.option('-id', prompt="Enter your student ID")
@click.option('--password', prompt=True, hide_input=True)
def test(id, password):
    obj = hibterm.Student(id, password)
    success = obj.student_login()
    if success:
        obj.student_greeting()
    else:
        click.echo(click.style(
            "Incorrect Credentials! Try again.\n", fg="bright_red"))


if __name__ == '__main__':
    test()
