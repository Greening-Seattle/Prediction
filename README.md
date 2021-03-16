# Greening Seattle, the Making (Prediction Modeling)
# Team Members: Praise Anyanwu, Brendan Butler, Matthew Canin, Nicolas Wittstock

[![Build Status](https://travis-ci.org/Greening-Seattle/Prediction.svg?branch=main)](https://travis-ci.org/Greening-Seattle/Prediction)

[![Coverage Status](https://coveralls.io/repos/github/Greening-Seattle/Prediction/badge.svg?branch=main)](https://coveralls.io/github/Greening-Seattle/Prediction?branch=main)

## Welcome!
**Version 1.0.0**

In the City of Seattle, transportation accounts for 60% of total core emissions, 61% of which are attributed to
gasoline/diesel sources. Population increased by 25% from 2008 - 2018, and is expected to continue at the same rate
(if not faster). The effects of this increase will be felt by our existing infrastructure and transportation systems,
such as our bus system. Citizen survey data indicates a push for Seattle transportation to be more robust and equitable.
As a functioning unit, accessible transportation lies at the interface of social, environmental and economic justice.

The overrarching goal of this software is therefore to use historic traffic patterns in Seattle over the past 10+ years in
order to inform citizens, policymakers, or environmental groups of how traffic throughout the City is projected to change
in response to our constantly changing urban landscape. Specifically, for a given zip code (or set of zip codes), users will
be able to generate predicted traffic flow in region in a future year. This software works by training an artificial neural network
in TensorFlow on  historic traffic flow by region as a function of urban feautres (population, bike rack capacity, and bike lane lengths).
We chose to utilize an artificial NN because we determined from statistical analysis that features are not linearly related to each other
over time and space. The neural network takes the 2018 feature data from an input zip code and projects changes in traffic based on proportional
increases in the input values. In short, the user can estimate changes in traffic flow for an input zip code based on % changes in:
  
         i. Population
      
         ii. Bike rack capacity
      
         iii. Length of bike lanes
     
## Architecture of Repository
```
|   README.md
|   LICENSE
|   .travis.yml
|   .gitignore
|
+---doc
|   |   Use_Cases.md
|
+---greenseattle
|   |   __init__.py
|   |   greenseattle.py
|   |   greendata.py
|   |   Demo.ipynb
|   |   zips_show.py
|   |
|   +---tests
|   |   __init__.py
|   |   test_greenseattle.py
|   |   test_greendata.py
|   \---data
|           all_data.csv
|           Population_Traffic_2017_NW.csv
|           testing.csv
|           Weights_MultiFeatures.pckl
```

## Software Packages

### ***Traffic modeling package***
* `greenseattle.py`: trains on csv file output by data loading package and predicts based on user-input feature changes

### ***Data loading package***
* `greendata.py`: loads in datasets, cleans and merges data, and outputs a csv file with all features and target data

**Wrapping function**
* `get_alldata()`: returns dataframe of aggregated features and target data

**Geographical boundary data**
* `get_tracts()`: returns dataframe of census tract boundaries
* `get_tractcenters()`: returns dataframe of census tract centroids
* `get_zips()`: returns dataframe of zip code boundaries

**Urban features**
* `get_racks()`: returns dataframe of bike rack capacities by zip code and year
* `get_lanes()`: returns dataframe of bike lane lengths by zip code and year
* `get_pop()`: returns dataframe of population by zip code and year

**Target**
* `get_alltraffic()`: returns dataframe of traffic volume by zip code and year
