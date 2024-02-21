import click
from evaluator import Evaluator
from utils import *

@click.command()
@click.option(
        "--file_path",
        required = False,
        type = str,
        help = "path where the tests are stored"
)
def main(file_path : str):
    eval = Evaluator()
    with open(file_path, 'r', encoding = 'utf-8') as f:
        for line in f:
            print(eval.run_evaluator(line))


if __name__ == '__main__':
    main()