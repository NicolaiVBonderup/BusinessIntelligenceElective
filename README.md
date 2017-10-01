# Business Intelligence Elective

This is a repository for the assignments given in the Business Intelligence elective of the second semester of the top-up bachelor program in Software Development at CPH Business Academy.

Assignment hand-ins displayed on this repository are group hand-ins for the group Disgusting Software, consisting of Emil Rosenius Pedersen, Theis Rye and Nicolai Vikkelsø Bonderup.

# Assignment 4: Data Visualization

## Dependencies
Running the script requires the installation of the following dependencies: 
- [Folium](https://folium.readthedocs.io/en/latest/)
- [MatPlotLib](https://matplotlib.org/)
- ​[pandas](http://pandas.pydata.org/)

## How to run

The script has no custom arguments, and will simply generate every chart requested for the assignment. To run the script, navigate to the `Assignment4` folder, and run the following:

```bash
$ py -u main.py
```

Running this script will populate the directory `data` with all of the results.



## Results

#### Basemap

![basemap](https://raw.githubusercontent.com/NicolaiVBonderup/BusinessIntelligenceElective/master/Assignment4/data/copenhagen_haver.png)

#### Folium

[Full HTML page](https://raw.githubusercontent.com/NicolaiVBonderup/BusinessIntelligenceElective/master/Assignment4/data/large_flat_trades.html) is available in the results folder in Assignment 4.

#### Nørreport Price Effect

- *Formulate a hypothesis on how the values on the two axis might be related*

The graph shows that the closer the dwelling lies to Nørreport Station, the higher the price per square meter becomes. There's a few different reasons for why this is the case: 

Accessibility of public transportation is often a large factor in the desirability of a house or apartment, especially in a greater metropolitan area where transportation by car is often more difficult and time-consuming due to traffic. 

Also, Nørreport is situated in the heart of Copenhagen, and being that the price of a home usually increases the closer it is to a larger city, especially a capital city, it stands to reason that the price would increase even within the limits of the city itself.

![nørreport](https://raw.githubusercontent.com/NicolaiVBonderup/BusinessIntelligenceElective/master/Assignment4/data/norreport_sales.png)

#### Sales by Zipcode Histogram

*Large image*

![sales](https://raw.githubusercontent.com/NicolaiVBonderup/BusinessIntelligenceElective/master/Assignment4/data/sales_by_zip.png)

#### Cumulative Stacked Histogram

![stackedhist](https://raw.githubusercontent.com/NicolaiVBonderup/BusinessIntelligenceElective/master/Assignment4/data/histogram_by_rooms.png)

#### 3D Histogram

![3d](https://raw.githubusercontent.com/NicolaiVBonderup/BusinessIntelligenceElective/master/Assignment4/data/sales_by_zip_3d.png)

#### Freestyle

People in the big city are usually people on the go: Well-paying jobs, very important people, but also very busy people. They don't have no time for cooking, ![so they're much more likely to eat fast food](https://www.ncbi.nlm.nih.gov/pubmed/28472714). Using statistics, we can show that very wealthy people value accessibility of fast food very highly. 

Shown here, we have calculated the average price per square meter of every home, along with the distance to the nearest Kentucky Fried Chicken in Copenhagen:

![kfc](https://raw.githubusercontent.com/NicolaiVBonderup/BusinessIntelligenceElective/master/Assignment4/data/kfc_sales.png)

As you can see, the closer you get, the more expensive it becomes. Also, it seems that the point at which someone becomes interested in the proximity of the nearest Kentucky Fried Chicken pivots *very* dramatically at a certain point. As such, when you're planning your new multi-million DKK housing complex, consider placing it nearby a KFC.

Also no, we've never heard of the [correlation/causation fallacy.](https://en.wikipedia.org/wiki/Illusory_correlation)
