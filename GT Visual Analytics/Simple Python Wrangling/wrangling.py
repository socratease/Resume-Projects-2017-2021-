""" wrangling.py - utilities to supply data to the templates.

This file contains a pair of functions for retrieving and manipulating data
that will be supplied to the template for generating the table."""
import csv

def username():
    return 'cgraves36'

def data_wrangling():
    with open('data/movies.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        table = list()
        rowcount = 0
        ...
        
        # Read in the header
        for header in reader:
            break
        
        # Read in each row
        for row in reader:
            if rowcount < 101: 
                table.append(row)
                rowcount += 1
            else:
                break
            # Only read first 100 data rows - [2 points] Q5.a
        table = sorted(table, key=lambda x: int(float(x[len(x)-1])), reverse = True)
        # Order table by the last column - [3 points] Q5.b
        ...
    
    return header, table

