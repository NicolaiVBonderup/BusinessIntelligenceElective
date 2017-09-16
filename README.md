# Business Intelligence Elective

This is a repository for the assignments given in the Business Intelligence elective of the second semester of the top-up bachelor program in Software Development at CPH Business Academy.

Assignment hand-ins displayed on this repository are group hand-ins for the group Disgusting Software, consisting of Emil Rosenius Pedersen, Theis Rye and Nicolai Vikkelsø Bonderup.

# Assignment 2: Data Collection

The webscraper we have written for scraping the data off of the Boliga mirror was written using the Scrapy framework, instead of Beautiful Soup. The contents of the [boliga folder](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/tree/master/boliga) contain all of the necessary project and setup files for Scrapy to function, along with the Python script file [sales.py](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/blob/master/boliga/boliga/spiders/sales.py) in the folder [spiders](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/tree/master/boliga/boliga/spiders), which contains our webscraper script.

## Dependencies
Running the scraper script requires the installation of the following dependencies: 
- [Scrapy](https://scrapy.org/)
- [Microsoft Visual C++ Build Library](http://landinghub.visualstudio.com/visual-cpp-build-tools)
- [tqdm](https://github.com/tqdm/tqdm)
- [pywin32](https://sourceforge.net/projects/pywin32/). 

## How to run
To run the scraper, creating a .CSV file in the working directory with the results, execute the following command anywhere inside the [boliga folder](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/tree/master/boliga):

```bash
$ scrapy runspider sales --nolog
```

*The* `--nolog` *modifier can be left off in order to see realtime logs from the scraper, but it will flood the console with a log from Scrapy for every site opened.*

### Arguments
We have also added custom arguments to the script. Being that we are running through the Scrapy framework, we could not use the standard `argparse` module, but instead used the argument `-a` built into the Scrapy framework to introduce custom arguments.

#### zip_split
`zip_split` takes either a 'yes' or 'no', alternatively 'y' or 'n', which determines if the scraped data should be split into CSV files separated by zipcode, or kept in one big CSV file.

## Assignments

### How many sales records are there per zip code area? How many in total? 

In order to produce this data, we ran our Python script with the option to generate separate CSV files for every zipcode. Thereafter, we ran the following bash command:

```bash
$ find . -name '*.csv' | xargs wc -l >> sales_results.txt
```

This command finds every file ending with the extension `.csv`, and prints the linecount of each file into the file 'sales_results.txt'.

The full results are available in the file [sales_results.txt](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/blob/master/sales_results.txt). The full linecount of every sales record is **1,277,014**.


### For which zip code area do you have the most sales records?

For this, we use the same zipcode-separated CSV files, and execute the following bash commands to sort all files by word count, and pick out the file at the top:

```bash
$ find . -name "*.csv" -type f | xargs wc -l | sort -rn | grep -v ' total$' | head -1
```

We `find` a file in the working directory, matching it by its `-name`, which is a regular file, so we add `-type f`. We then use `xargs` to execute commands, such as `wc -l` to count the lines of each document. We then `sort -rn` to reverse and numerically sort the files by their linecount, `grep -v ' total$'` to remove the 'total' line that `wc` generates, and `head -1` to only display the first result at the top of the list.

The result of this command is:

`17405 ./2300.csv`

As such, we know that 2300.csv is the largest file, containing 17,405 records, meaning that apparently people **really** want to sell their homes and move away from København S. We can now use `du` to calculate the disk usage of a file:

`du -k 2300.csv`

This will give us the result:

`1700 2300.csv`

This means that the file contains 1700KB of data.

### For which zip code area do you have the fewest sales records?

For this, we repeat the process of the last assignment, but with a small tweak to the script, replacing `head` with `tail` so that we get the last result in the sorted list.

`find . -name "*.csv" -type f | xargs wc -l | sort -rn | grep -v ' total$' | tail -1`

The result of this command is;

`1 ./1061.csv`

This means that the file contains ~1MB of data.
