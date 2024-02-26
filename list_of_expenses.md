# List of expenses


This code helps you to easy calculate daily expenses and generate raports. Every expense has ID, description and amount of cash.

This code has a few commands such as:

- add - it allows you to add new expense. To provide new expense after command you need to provide amount in `int` formula and description, for example 
```sh
python filename.py add 100 "description_of_expense"
```
ID will be automatically assign to new enter by checking the next highest ID already exist.

- report - it allows you to show every expense already entered as a report in terminal  in form of list
- export-python - it allows to show list of expense as object
- import-csv - it allows import expenses from `.csv` file

Code in between of starting stores data in file `expenses.db`. If it doesn't exists it creates new one.

The code also is checking if provided amount is positive or negative. If negative it raise an error.