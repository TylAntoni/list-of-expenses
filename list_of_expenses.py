from dataclasses import dataclass
from typing import List
import click
import sys
import pickle
import csv

@dataclass
class Expenses:
    id: int
    value: int
    description: str

    def __post_init__(self):
        if self.value < 0:
            raise ValueError('Wydatek nie może być ujemny!')
    
    def is_big(self) -> bool:
        return self.value > 1000

EXP_FILE_DB = 'expenses.db'


def load_or_init_expanse() -> List[Expenses]:
    try:
        with open(EXP_FILE_DB, 'rb') as stream:
            expenses = pickle.load(stream)
    except FileNotFoundError:
        expenses = []
    return expenses

def save_file_expanse(expenses: List[Expenses]) -> None:
    with open(EXP_FILE_DB, 'wb') as stream:
        expenses = pickle.dump(expenses, stream)

def finding_new_id(expenses: List[Expenses]) -> int:
    ids = {exp.id for exp in expenses}
    counter = 1
    while counter in ids:
        counter += 1
    return counter

def sum_up_values(expenses: List[Expenses]) -> int:
    values = [s.value for s in expenses]
    return sum(values)

def print_expenses(expenses: List[Expenses], total: int) -> None:
    print('  ID  EXPENSE  BIG  DESCRITPION')
    if expenses:
        for exp in expenses:
            if exp.is_big():
                big = '+'
            else:
                big = ' '
            print(f'{exp.id:4}  {exp.value:^7}  {big:^3}  {exp.description}')
        print(f'Total value of expenses -> {total}')
    
    else:
        print('Niewprowadzono żadnych wydatków!')

@click.group()
def cli():
    pass

@cli.command()
def raport() ->None:
    expenses = load_or_init_expanse()
    total_expenses = sum_up_values(expenses)
    print_expenses(expenses, total_expenses)


@cli.command()
@click.argument('value', type=int)
@click.argument('description')
def add(value: int, description: str):
    expenses = load_or_init_expanse()
    next_id = finding_new_id(expenses)
    try:
        new_task = Expenses(
            id=next_id,
            value=value,
            description=description
        )
    except ValueError as e:
        print(f'Błąd wpisu {e.args[0]}')
        sys.exit(1)
    
    expenses.append(new_task)
    save_file_expanse(expenses)
    print('Zapisano do pliku!')

@cli.command()
@click.argument('csv_file')
def import_csv(csv_file: str) -> None:
    expenses = load_or_init_expanse()
    try:
        with open(csv_file, 'r') as stream:
            csv_ = csv.DictReader(stream)
            for row in csv_:
                exp = Expenses(
                    id=finding_new_id(expenses),
                    value=float(row['amount']),
                    description=row['description']
                )
                expenses.append(exp)
    except FileNotFoundError:
        print('Nie znaleziono pliku!')
        sys.exit(1)
    
    save_file_expanse(expenses)
    print('Zapisano')

@cli.command()
def export_python() -> None:
    expenses = load_or_init_expanse()
    print(expenses)

if __name__ == "__main__":
    cli()

