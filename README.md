# Traffic Prediction

[![Build Status](https://travis-ci.org/Greening-Seattle/Prediction.svg?branch=main)](https://travis-ci.org/Greening-Seattle/Prediction)

[![Coverage Status](https://coveralls.io/repos/github/Greening-Seattle/Prediction/badge.svg?branch=main)](https://coveralls.io/github/Greening-Seattle/Prediction?branch=main)

## Welcome to Greening Seattle, the Modeling!

The overrarching goal of this software is to inform citizens, policymakers, or environmental groups of
how traffic flow patters throughout the City are projected to change in response to current and historical
trends in a variety of urban features. As a user of our software, you will be able to:

  1. Calculate how traffic flows have in increased over two prior years for a given Census tract region of Seattle 
  2. For a specific Census tract region, generate predicted traffic flow in region in a future year 
  3. Estimate changes in traffic flow based on % changes in the following features over the next _N_ years:
  
      i. Bike lanes
     ii. Parking spaces
    iii. Light rail addition
 
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
