import click
from evaluator import Evaluator


@click.command()
@click.option(
    "--file_path",
    required=False,
    type=str,
    help="path where the tests are stored"
)
@click.option(
    "--repl",
    is_flag=True,
    help="if repl than you can test it from terminal"
)
def main(file_path: str,
         repl: bool):
    eval = Evaluator()
    if file_path is not None:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                eval.run_evaluator(line)
    if repl:
        eval.repl()


if __name__ == '__main__':
    main()
