# Business Intelligence Elective

This is a repository for the assignments given in the Business Intelligence elective of the second semester of the top-up bachelor program in Software Development at CPHBusiness.

Assignment hand-ins displayed on this repository are group hand-ins for the group Disgusting Software, consisting of Emil Rosenius Pedersen, Theis Rye and Nicolai Vikkelsø Bonderup.

# Assignment 2: Data Collection

The webscraper we have written for scraping the data off of the Boliga mirror was written using the Scrapy framework, instead of Beautiful Soup. The contents of the [boliga](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/tree/master/boliga) folder contain all of the necessary project and setup files for Scrapy to function, along with the Python script file [sales.py](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/blob/master/boliga/boliga/spiders/sales.py) in the folder [spiders](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/tree/master/boliga/boliga/spiders), which contains out scraper script.

Running the scraper script requires the installation of [Scrapy](https://scrapy.org/), the [Microsoft Visual C++ Build Library](http://landinghub.visualstudio.com/visual-cpp-build-tools), [tqdm](https://github.com/tqdm/tqdm) and [pywin32](https://sourceforge.net/projects/pywin32/). Once the required dependencies are installed, navigate to the [spiders](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/tree/master/boliga/boliga/spiders) directory, and execute this command:

`scrapy runspider sales.py --nolog`

This will run the scraper, creating a .CSV file in the working directory with the results. The `--nolog` modifier can be left off in order to see realtime logs from the scraper, but it will flood the console with a log from Scrapy for every site opened.


#### How many sales records are there per zip code area? How many in total? 

In order to produce this data, we ran our Python script with the option to generate separate CSV files for every zipcode. Thereafter, we ran the follow bash command:

`find . -name '*.csv' | xargs wc -l >> sales_results.txt`

The full results are available in the file [sales_results.txt](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/blob/master/sales_results.txt). The full linecount of every sales record is *insert when finished*


#### For which zip code area do you have the most sales records?

For this, we use the same zipcode-separated CSV files, and execute the follow bash commands to sort all files by word count, and pick out the file at the top:

`find . -name "*.csv" -type f | xargs wc -l | sort -rn | grep -v ' total$' | head -1`

We `find` a file in the working directory, matching it by its `-name`, which is a regular file, so we add `-type f`. We then use `xargs` to execute commands, such as `wc -l` to count the lines of each document. We then `sort -rn` to reverse and numerically sort the files by their linecount, `grep -v ' total$'` to remove the 'total' line that `wc` generates, and `head -1` to only display the first result at the top of the list.

The result of this command is:

`13722 ./8700.csv`

As such, we know that 8700.csv is the largest file, containing 13,722 records.

`du -k 8700.csv`

This will give us the result:

`1124 8700.csv`

This means that the file contains 1124Kb of data.

#### For which zip code area do you have the fewest sales records?

For this, we repeat the process of the last assignment, but with a small tweak to the script, replacing `head` with `tail` so that we get the last result in the sorted list.

`find . -name "*.csv" -type f | xargs wc -l | sort -rn | grep -v ' total$' | tail -1`

The result of this command is;

``

and the total size of this file is:

``



