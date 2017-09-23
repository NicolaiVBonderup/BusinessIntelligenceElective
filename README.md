# Business Intelligence Elective

This is a repository for the assignments given in the Business Intelligence elective of the second semester of the top-up bachelor program in Software Development at CPH Business Academy.

Assignment hand-ins displayed on this repository are group hand-ins for the group Disgusting Software, consisting of Emil Rosenius Pedersen, Theis Rye and Nicolai Vikkelsø Bonderup.

# Assignment 3: Data Processing

The webscraper we have written for scraping the data off of the Boliga mirror was written using the Scrapy framework, instead of Beautiful Soup. The contents of the [boliga folder](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/tree/master/boliga) contain all of the necessary project and setup files for Scrapy to function, along with the Python script file [sales.py](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/blob/master/boliga/boliga/spiders/sales.py) in the folder [spiders](https://github.com/NicolaiVBonderup/BusinessIntelligenceElective/tree/master/boliga/boliga/spiders), which contains our webscraper script.

## Dependencies
Running the script requires the installation of the following dependencies: 
- [osmconvert](https://wiki.openstreetmap.org/wiki/Osmconvert)
- [XML_Breaker.py](https://gist.github.com/nicwolff/b4da6ec84ba9c23c8e59)
- [tqdm](https://github.com/tqdm/tqdm)

## How to run

Due to difficulties with parsing the full OSM file consuming too much memory, I've elected to trim and separate the file into smaller, more manageable chunks, and then reading them sequentially.

First, I downloaded the binary for [osmconvert](https://wiki.openstreetmap.org/wiki/Osmconvert), and adding it to the PATH of my CLI. In my case, I use Git Bash, so I renamed the file to simply `osmconvert` and added it to the `Git/mingw64/bin` directory.

Once I had `osmconvert` available, I moved to the directory where my .OSM file was, and ran the following command:

```bash
$ osmconvert denmark-latest.osm --drop-ways --drop-relations > trimmed-denmark-latest.osm
```

Running this command takes the OSM file, and writes it to a new file, `trimmed-denmark-latest.osm`, but leaving out all `<way>` and `<relation>` elements, reducing the size of the file by almost a full gigabyte.

Afterwards, I split the file into several files using the [XML_Breaker.py](https://gist.github.com/nicwolff/b4da6ec84ba9c23c8e59) script. This script takes the provided file, and splits it at a provided line threshhold, but with consideration taken to not splitting the file in the middle of an element.

In this case, I wanted to split the file between `<node>` elements, and I wanted the files small enough to be manageable, so I ran it with the following commands:

```bash
$ py -2 XML_breaker.py trimmed-denmark-latest.xml node 2000000
```

This way, I split it every 2,000,000 lines, but only between `</node>` and `<node>` tags.

Be aware that this script is written in Python 2.7, and as such will not run normally with Python 3.6 installed. Therefore, add the following to the top of the script before running:

```python
#! /usr/bin/env python2
```
The memory footprint of this script is virtually non-existent, so I'm likely going to attempt to rewrite it in Python 3.6 once I've finished the assignment, to see if I can't figure out how to do this kind of file processing without memory issues.