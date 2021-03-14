# Greening Seattle, the Making (Prediction Modeling)

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
in response to our constantly changing urban landscape. Specifically, users will be able to:

  1. Calculate how traffic flows have in increased over two prior years for a given region of Seattle, specified by zip code. 
  
  2. For a specific zip code, generate predicted traffic flow in region in a future year. 
  
  3. Estimate changes in traffic flow based on % changes in the following features over the next _N_ years:
  
         i. Bike lanes
      
         ii. Bike racks
      
         iii. Walkways
    
         iv. Population
 
[Use case graphic](brendanbutler.github.com/Greening-Seattle/Prediction/img/Slide1.jpg)

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
|   |
|   +---tests
|   |   __init__.py
|   |   test_greenseattle.py 
|   \---data
|           testing.csv
```
