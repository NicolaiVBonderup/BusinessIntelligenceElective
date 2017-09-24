# Business Intelligence Elective

This is a repository for the assignments given in the Business Intelligence elective of the second semester of the top-up bachelor program in Software Development at CPH Business Academy.

Assignment hand-ins displayed on this repository are group hand-ins for the group Disgusting Software, consisting of Emil Rosenius Pedersen, Theis Rye and Nicolai Vikkelsø Bonderup.

# Assignment 3: Data Processing

## Dependencies
Running the script requires the installation of the following dependencies: 
- [osmconvert](https://wiki.openstreetmap.org/wiki/Osmconvert)
- [XML_Breaker.py](https://gist.github.com/nicwolff/b4da6ec84ba9c23c8e59)
- [tqdm](https://github.com/tqdm/tqdm)
- ​[pandas](http://pandas.pydata.org/)
- ​[NumPy](http://www.numpy.org/)
- [osmread](https://github.com/dezhin/osmread)

## Preparation

Due to difficulties with parsing the full OSM file consuming too much memory, we've elected to trim and separate the file into smaller, more manageable chunks, and then reading them sequentially.

First, we downloaded the binary for [osmconvert](https://wiki.openstreetmap.org/wiki/Osmconvert), and added it to the PATH of our CLI. In our case, we use Git Bash, so we renamed the file to simply `osmconvert` and added it to the `Git/mingw64/bin` directory.

Once we had `osmconvert` available, we moved to the directory where the .OSM file was, and ran the following command:

```bash
$ osmconvert denmark-latest.osm --drop-ways --drop-relations > trimmed-denmark-latest.osm
```

Running this command takes the OSM file, and writes it to a new file, `trimmed-denmark-latest.osm`, but leaving out all `<way>` and `<relation>` elements, reducing the size of the file by almost a full gigabyte.

Afterwards, we split the file into several files using the [XML_Breaker.py](https://gist.github.com/nicwolff/b4da6ec84ba9c23c8e59) script. This script takes the provided file, and splits it at a provided line threshhold, but with consideration taken to not splitting the file in the middle of an element.

In this case, I wanted to split the file between `<node>` elements, and I wanted the files small enough to be manageable, so I ran it with the following commands:

```bash
$ py -2 XML_breaker.py trimmed-denmark-latest.xml node 2000000
```

This way, we split it every 2,000,000 lines, but only between `</node>` and `<node>` tags.

Be aware that this script is written in Python 2.7, and as such will not run normally with Python 3.6 installed. Therefore, add the following to the top of the script before running:

```python
#! /usr/bin/env python2
```
The memory footprint of this script is virtually non-existent, so it would be a good idea to attempt to recreate it in Python 3.6 some time, to see if we can't figure out how to do this kind of file processing without memory issues.

## How to run

Once this is all done, move the split-up osm/xml files to the `data` folder, and place the `boliga_prices.csv` file from the previous assignment in the same folder as `main.py`. Would've liked to add custom arguments for choosing paths, but we ran out of time due to a lot of unforeseen issues encountered throughout this assignment.

Once the files are in place, simply run the script:

```bash
$ py -u main.py
```

Running this script creates a directory, `geodata`, which is then populated by four new files:

- `geolocated_data.csv`, which is similar to `boliga_prices.csv`, but with latitude and longitude added.
- `addr_with_geo.csv`, which is a csv file containing all addresses with their corresponding latitudes and longitudes found in the .osm file.
- `datetime_data.csv`, which is `geolocated_data.csv`, but with the `sell_date` column converted to `datetime64`.
- `mean_sales.csv`, which contains the mean price per square inch of all sales in København, Odense, Aarhus and Aalborg in the years 1992 and 2016.

Along with these csv files, two image files are also created in the working directory; `latlongscatter.png` and `roskildescatter.png`. These are the scatter plots generated through the sales data.

## Results

#### Mean Price Per Square Meter

The mean prices per square meter of the four specified cities were calculated as such:

|               | 1992              | 2016              |
| ------------- | ----------------- | ----------------- |
| **København** | 19.68113888888889 | 44.13184375       |
| **Odense**    | 5.452180722891566 | 19.1051107266436  |
| **Aarhus**    | 12.889            | 44.49854609929078 |
| **Aalborg**   | 8.167764285714286 | 22.21893777777778 |

#### Scatter Plots

**Scatter plot without haversine coloring:**

![scatter1](https://raw.githubusercontent.com/NicolaiVBonderup/BusinessIntelligenceElective/master/Assignment3/latlongscatter.png)

**Scatter plot with haversine coloring:**

![scatter2](https://raw.githubusercontent.com/NicolaiVBonderup/BusinessIntelligenceElective/master/Assignment3/roskildescatter.png)
