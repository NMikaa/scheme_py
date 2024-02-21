
# Scheme Interpreter in python

This project is a Scheme interpreter implemented in Python. It is designed to emulate the core functionalities of the Scheme programming language, providing a lightweight and efficient platform for executing Scheme code.

## Features
- **Lambda Functions**: Support for anonymous function creation using the `lambda` keyword.
- **Immediate Lambda Invocation**: Capability to define and immediately execute lambda functions.
- **Variable and Function Definitions**: Utilize the `define` keyword for binding values to names and for function definitions.
- **Conditional Logic**: Implementation of `if/else` statements for conditional execution.
- **List Processing**: A suite of functions for list manipulation including `car`, `cdr`, `cons`, `map`, and `append`.
- **Quoted Lists**: Ability to interpret list descriptions without execution, essential for list management.
- **Executive Functions**: Functions like `apply` and `eval` to dynamically execute code.
- **Recursive Functions**: Support for functions that call themselves, enabling complex algorithmic implementations.
- **Auxiliary Functions**: Includes utility functions like `null?` and `length` for additional data handling capabilities.
## requirements

- You are going to need Python 3.0 or higher to run this.
- also, for satisfying the requirements you can run ```pip install -r requirements.txt``` in your terminal
## Getting Started
you can just clone the repository, go to your terminal, and run the file like this:
**NOTE! THERE ARE EXACTLY TWO VARIABLES IN MAIN.** 
- **FIRST**: ```--file_path```. If you want to run my Scheme interpreter on your tests, your tests should be separated each on one line and should be written in .txt file. (for example, visit lunar_test.txt). Using this variable is not required, therefore you can ignore it.
- **SECOND**: ```--repl```. If you want to run my Scheme interpreter and play with it, you can just pass this argument by itself, it is a boolean type so if you pass it you can just enter the KAWA WORLD!
### EXAMPLE USAGES!
1. ```python -m main --file_path "your_test_file.txt" --repl```. 
2. ```python -m main --repl```
first will first run your tests and then open the playground, second will straight up open the playground!


****Happy Coding!****




