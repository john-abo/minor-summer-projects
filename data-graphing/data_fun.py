#!/usr/bin/python3

'''
███
So I think I can generate reports using this program
Lets take advantage of the colored drawing libraries

Sourced some datasets from https://data.calgary.ca
used for testing. Data is not included

The assumption is also that the dataset is already cleaned. I don't want to have to clean them but I'll worry about it once it arises

***File names***:
    Public_Water_Main_20240515.csv
    Public_Sanitary_Service_Lines_20240518.csv
    Traffic_Volumes_for_2022_20240518.csv

Some general TODO that I want to do with this code:
-   Put this all into an object. So we can make this into a module I can use in 
    other programs. If anything, at least as a debug tool. But maybe other stuff
-   Another render function, where we use a proper UI library to draw more accurate
    user friendly reports. but for now? terminal chads.
-   What else do I want to do? I can't even think lmao
'''

import csv
from termcolor import colored

# Metadata and actual data
# Is this efficient? of course not
# Will this let me manipulate the data as I see fit? most likely? I hope
# Also global variables. Because I love bad practice
meta = []
data = {}
row_count = 0
dimensions = 20

# TODO this renders the aggregated data into a series of bar graphs. Limits the number of rows.
# Aggregated data is assumed to be a list
# For now, it only knows bar graphs. But I'd like it to know how to do other forms of reports
# Limit default to 10 rows of the aggregated data
#
# I like to think this is a fairly robust function
# Since it simply draws any list of numbers. I can export this
# 
# I now want it to render different types of graphs? Maybe points would be cool too? then I can use periods
# And maybe even take it to the next level to get lines? THAT would be wild
#
# Lets make this account for other modes, I want this to work for other forms
# of data. I Wonder if I can make this into a basic graphics engine
def render(aggregate, limit=10, mode='bar'):

    # max and min values used to render upper and lower limits
    # The question is. What do we do with negative values?
    # Maybe we can test with sample aggregations
    # This should change the aggregate array to meet the limit
    aggregate = aggregate[:limit]
    max = aggregate[0]
    min = aggregate[0]

    for cell in aggregate:
        if cell > max:
            max = cell
        if cell < min:
            min = cell

    # ok well, lets map the values ourselves??
    
    diff = max - min
    jump = int (diff / dimensions) + 1
    data_range = []

    for i in range(dimensions):
        data_range.append((i * jump) + min)

    data_range.reverse()

    #print(aggregate)
    #print(data_range)
    #print(f'{max}, {min}, {diff}, {jump}')

    # Generate a bar graph in the terminal
    if mode == 'bar':
        for i in range(dimensions):
            row = ''
            row += colored(str(int(data_range[i])), 'red') + '\t|'

            # I think I need to add some logic if the value of a certain data_range is less than 0.
            for j in range(len(aggregate)):
                if data_range[i] >= 0:
                    if aggregate[j] >= data_range[i] and aggregate[j] >= 0:
                        row += colored('█', 'green')
                    else:
                        row += ' '
                else:
                    if aggregate[j] <= data_range[i] and aggregate[j] < 0:
                        row += colored('█', 'red')
                    else:
                        row += ' '
                    pass
            print(row)

# TODO Finds the frequencies of all unique entries in a column
# This can be good from some baynesian shenanigans
def freq(col):
    pass

# TODO Finds all rows with a certain pattern
def find(col, pattern):
    pass

# TODO finds the average value of this column
def average(col):
    pass

# TODO I wonder if I can get it to sort based on the column?
# More than just a sort, sorts a multicolumn table
def sort(col):
    pass

# This draws a number rows of the data set
# mostly for debugging stuff lul  
def data_table(rows):
    print(colored(f'Printing {rows} row(s) of data', 'white', 'on_green'))

    for i in range(rows):
        if i > rows:
            break

        println = ""
        for col in meta:
            println += data[col][i]
            println += ', '
            pass
        println = println[:-1]

        print(println)

# Parses the CSV file for data
def parser(filename):

    global meta
    global data
    global row_count
    
    try:
        print(colored('Sample file read...', 'green', 'on_black'))
        with open(filename, mode='r') as file:
            reader = csv.reader(file)

            # This is just to extract metadata and 
            for i, row in enumerate(reader):
                # Print the first five rows
                if i < 5:
                    #print(row)
                    pass

                # Saves metadata and data
                if i == 0:
                    meta = row
                    for attribute in meta:
                        data[attribute] = []
                else:
                    for j, col in enumerate(row):
                        data[meta[j]].append(col)
                
                    #print(f'Adding row, {i}')
                    row_count += 1

        print(colored('File read!', 'green', 'on_black'))
    except Exception as e:
        print(f'File reading error!:\n{e}')

# Prints a manual. I can write a README that contains the directions for each file
# Take it a step further? Read a SECTION of the README based on flags? I think that'd be sick actually
# And would probably just involve flag
def manual():
    print(colored('Here is the manual nerd', 'white', 'on_red'))
    start_flag = False
    i = 0
    try:
        with open('readme.txt', 'r') as file:
            for line in [l.strip() for l in file.readlines()]:
                if line == '///':
                    if start_flag:
                        start_flag = False
                    else:
                        start_flag = True
                elif start_flag:
                    print(line)
                else:
                    i += 1
    except Exception as e:
        print('What happened?')
        print(e)
    
    #print(f'{i} lines skipped')

# TODO This prints some meta data, including file sizes
# I should refactor this to be an object maybe
# That way I can really turn this into a library for parsing data in other programs
# But for now. No.
def get_meta():
    print(colored('=== META DATA ===', 'white', 'on_green'))
    print('Columns')
    print(meta)
    print(f'Data contains {row_count} row(s)')
    pass

# Main lmao
if __name__ == '__main__':
    print(colored('Some data shenanigans', 'white', 'on_green'))
    csv_name = input('Filename: ').strip()

    # open the csv to get the data
    # Should make this a user input tho
    filename = f'/data/{csv_name}'
    parser(filename)

    print(f'Number of rows found {row_count}')

    #print(colored('Testing render', 'white', 'on_green'))
    #render([-1,1,-2,2,-3,3,5,-7.1])

    # Gives user options
    while True and row_count > 0:
        user_in = input('>').strip().lower().split(' ')
        #print(f'Debut input: {user_in}')

        print(f'USER IN: {user_in}')

        try:
            if user_in[0] == 'exit':
                break
            if user_in[0] == 'print':
                data_table(int(user_in[1]))
            if user_in[0] == 'average' or user_in[0] == 'avg':
                average()
            if user_in[0] == 'render':
                aggregate = []
                print(colored(f'Extracting column {meta[int(user_in[1])]}', 'white', 'on_red'))
                for i in range (row_count):
                    aggregate.append(float(data[meta[int(user_in[1])]][i]))
                # DEBUG just to see the data in the first 10 rows of the column
                #print(aggregate)
                #for i in range(10):
                #    print(aggregate[i])
                try:
                    render(aggregate, limit=int(user_in[2]))
                except:
                    print(colored('No limit found. Default limit = 10', 'white', 'on_red'))
                    render(aggregate)
            if user_in[0] == 'sort':
                sort(int(user_in[1]))
            if user_in[0] == 'man':
                manual()
            if user_in[0] == 'meta':
                # I should make this into a function that gives a bunch of other supplemental data
                get_meta()
            if user_in[0] == 'freq':
                pass
            if user_in[0] == 'find':
                pass
        except Exception as e:
            print('Invalid input')
            print(e)
    print('Bye bye')