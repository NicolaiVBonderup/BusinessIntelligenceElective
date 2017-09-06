# Business Intelligence Elective

This is a repository for the assignments given in the Business Intelligence elective of the second semester of the top-up bachelor program in Software Development at CPHBusiness.

## Assignment 1

# Assignment 1: Environment Setup and Introduction to Python

    1. **List the all files that this program generates.**


The program generates two files: *price_list.csv* and *prices.png*.

2. **Describe which types of files this program generates and attach the contents of each file together with its name to your solution.**

The first file, *price_list.csv*, is created by reading the file *price_list.txt* and running it through a method that reads its contents and plots the data into a CSV format.

`generate_csv(txt_path, csv_path)`

Afterwards, it calls a method that utilizes the library `matplotlib`, which is a library providing plotting of statistical data onto a 2D  image, which is then exported as a `.png` file.

`generate_plot(data)`

3. **What is the output of this program?**

The average price of every property on the price list, calculated by the `compute_avg_price()` method. The output of the method is `3307228.119047619`.

4. **Describe in natural language and line-by-line what the program is doing. Describe also for each line what the Python code expresses.**


Pretty tempted to be more descriptive, but as far as I understand, 'natural language' means something non-technical, so I've tried to dumb it down as much as possible.

```
# These are imports, similar to imports in other languages, bringing in libraries for use in the program.
import os
import csv
import requests
import platform
import statistics
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


# Defines a method named 'download_txt()'.
def download_txt(url, save_path='./downloaded'):
    # Uses the 'requests' HTTP library to get the price_list.txt file from the course's GitHub repository.
    response = requests.get(url)
    # 'With' takes the result of the open() call, and assigns the result to the variable 'f'.
    # open() opens up a file, and the 'wb' part tells it how it should open the file up.
    with open(save_path, 'wb') as f:
        # This part writes the content of the response we got earlier to the file we just opened up.
        f.write(response.content)


# Defines a method named 'generate_csv()'.
def generate_csv(txt_input_path, csv_output_path):
    # 'With' takes the result of the open() call, and assigns the result to the variable 'f'.
    # open() opens up a file, and the 'encoding' part tells it the format of the file it's opening.
    with open(txt_input_path, encoding='utf-8') as f:
        # Records the contents of the file into the variable 'txt_content'.
        txt_content = f.readlines()

    # Creates a variable with a list of words inside.
    rows = [['street', 'city', 'price', 'sqm', 'price_per_sqm']]
    # Repeats a block of code for every line present in the variable 'txt_content' from earlier.
    for line in txt_content:
        # Looks for lines where a space and asterisk symbol follow each other, then removes those instances.
        line = line.rstrip().replace('  * ', '')
        # Creates three new variables, filling them with data from the line, separated by tabs on the line.
        address, price, sqm = line.split('\t')
        # Creates two new variables, filling them with data from the line, separated by ';' characters on the line.
        street, city = address.split('; ')
        # Calculates the price per square meter of the given property.
        price_per_sqm = int(price) // int(sqm)
        # Creates a tuple, meaning a list of values separated by commas.
        row = (street, city, price, sqm, price_per_sqm)
        # Adds the tuple to the collection 'rows' that we defined earlier.
        rows.append(row)

    # Checks if the system this script is being run on is a Windows system.
    if platform.system() == 'Windows':
        # Sets a variable for later to fit with Windows' way of formatting a UTF-8 file.
        newline = ''
    else:
        # Sets a variable for later to fit with Unix's way of formatting a UTF-8 file.
        newline = None

    # 'With' takes the result of the open() call, and assigns the result to the variable 'f'.
    # open() opens up a file, and the 'w','newline' and 'encoding' parts tell it the format of the file it's opening.
    with open(csv_output_path, 'w', newline=newline, encoding='utf-8') as f:
        # Creates an object that allows for writing CSV-formatted files.
        output_writer = csv.writer(f)
        # Repeats a code block for every tuple in the 'rows' variable.
        for row in rows:
            # Writes every tuple to the file we opened earlier in the 'with' code.
            output_writer.writerow(row)


# Defines a method named 'read_prices()'.
def read_prices(csv_input_path):
    # 'With' takes the result of the open() call, and assigns the result to the variable 'f'.
    # open() opens up a file, and the 'encoding' part tells it the format of the file it's opening.
    with open(csv_input_path, encoding='utf-8') as f:
        # Creates an object that can read a CSV file.
        reader = csv.reader(f)
        # Creates a variable for seemingly disposable columns in the tuple.
        _ = next(reader)

        # Creates a collection for indexes.
        idxs = []
        # Creates a collection for prices.
        prices = []
        # Repeats a code block for row that the 'reader' object finds in the file we gave the 'open()' call.
        for row in reader:
            # Gets the different values from the tuple, adding the disposable columns to the '_' variable,
            # and then adding the price that we're interested in to the 'price' variable.
            _, _, price, _, _ = row
            # Adds an index for the price, defined by the line number of the row we're looking at.
            idxs.append(reader.line_num)
            # Converts the price to a different data type, and adds it to the 'prices' collection.
            prices.append(int(price))

    # Gives us a iterable list of tuples, made up of the prices and their indexes.
    return list(zip(idxs, prices))


# Defines a method named 'computer_avg_price()'.
def compute_avg_price(data):
    # Takes the tuples in the 'data' variable, disposes of the index in a bogus variable,
    # and adds the price to a 'price' variable.
    _, prices = zip(*data)
    # Uses the 'statistics' library to compute the mean of all prices in the collection.
    avg_price = statistics.mean(prices)

    # 'With' takes the result of the open() call, and assigns the result to the variable 'f'.
    # open() opens up a file, and the 'w' and 'encoding' parts tell it the format of the file it's opening.
    with open('/tmp/avg_price.txt', 'w', encoding='utf-8') as f:
        # Writes the mean of the prices to a file.
        f.write(str(avg_price))

    # Retuns the mean price to us.
    return avg_price


# Defines a method named 'generate_plot()'.
def generate_plot(data):
    # Assigns the prices and their indexes to x and y variables so they can be plotted on a graph.
    x_values, y_values = zip(*data)
    # Creates an object with the 'matplotlib' library that represents a graphical statistical figure.
    fig = plt.figure()
    # Creates a scatter plot with the prices and their indexes.
    plt.scatter(x_values, y_values, s=100)
    # Saves the scatter plot to a .png file.
    fig.savefig('./prices.png', bbox_inches='tight')


# Defines a method named 'run()'.
def run():
    # Puts the URL for the price list we need to calculate into a more easily usable variable.
    file_url = 'https://raw.githubusercontent.com/datsoftlyngby/' \
               'soft2017fall-business-intelligence-teaching-material/master/' \
               'assignments/assignment_1/price_list.txt'
    # Gets the base name of the path we defined above, which in this case is 'price_list.txt'.
    txt_file_name = os.path.basename(file_url)
    # Adds the text './' to the base name we grabbed above.
    txt_path = os.path.join('./', txt_file_name)
    # Runs the method 'download_txt' that we defined earlier, giving it the location of the file,
    # and where we want the file to be saved.
    download_txt(file_url, txt_path)
    # Defines the name we want for the CSV file we'll be generating.
    csv_file_name = 'price_list.csv'
    # Gets the path for the current working directory, which is where this script is being run from.
    csv_path = os.path.join(os.getcwd(), csv_file_name)
    # Generates a CSV file from the txt file we grabbed earlier, and saves it to the directory.
    generate_csv(txt_path, csv_path)
    # Reads the prices from the CSV file we made.
    data = read_prices(csv_path)
    # Calculates the mean of the prices we found earlier.
    avg_price = compute_avg_price(data)
    # Prints out the mean of the prices.
    print(avg_price)
    # Creates a scatter plot of the prices, and puts it into a .png file for us.
    generate_plot(data)


# Checks if this script is being run by itself, or if it's imported by a different script.
# If it's not imported, then call the 'run()' method.
if __name__ == '__main__':
    run()

```

