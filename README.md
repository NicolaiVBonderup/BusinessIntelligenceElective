# Business Intelligence Elective

This is a repository for the assignments given in the Business Intelligence elective of the second semester of the top-up bachelor program in Software Development at CPHBusiness.

Assignment hand-ins displayed on this repository are group hand-ins for the group Disgusting Software, consisting of Emil Rosenius Pedersen, Theis Rye and Nicolai Vikkelsø Bonderup.

# Assignment 2: Data Collection

The webscraper we have written for scraping the data off of the Boliga mirror was written using the Scrapy framework, instead of Beautiful Soup. The contents of the [boliga](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/tree/master/boliga) folder contain all of the necessary project and setup files for Scrapy to function, along with the Python script file [sales.py](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/blob/master/boliga/boliga/spiders/sales.py) in the folder [spiders](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/tree/master/boliga/boliga/spiders), which contains out scraper script.

Running the scraper script requires the installation of [Scrapy](https://scrapy.org/), the [Microsoft Visual C++ Build Library](http://landinghub.visualstudio.com/visual-cpp-build-tools), [tqdm](https://github.com/tqdm/tqdm) and [pywin32](https://sourceforge.net/projects/pywin32/). Once the required dependencies are installed, navigate to the [spiders](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/tree/master/boliga/boliga/spiders) directory, and execute this command:

`scrapy runspider sales.py --nolog`

This will run the scraper, creating a .CSV file in the working directory with the results. The `--nolog` modifier can be left off in order to see realtime logs from the scraper, but it will flood the console with a log from Scrapy for every site opened.
