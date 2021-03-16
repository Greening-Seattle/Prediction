## Use Cases and Component Specifications of Traffic Model Predictor ##


## 1. Predict future traffic volumes by zip code. ##

**Users: Citizens, policy makers, environmental groups, city planners** 

Information provided by the user: Zip code of interest (map is visible to user), future year to predict AAWDT (Annual Average Weekday Traffic) flow. 

Response provided by the system: Projected percent increase AAWDT for a given year based on historical data within the specified zip code.
 
![Test Image 4](https://github.com/Greening-Seattle/Prediction/zip_show)

**Components and Sub-components:**
- **get_trafficdata: Function that regulates all traffic data downloads from Seattle.gov for processing**
	- get_alltraffic: Compiles all AAWDT data from 2007 - 2018 for use
- **green_model: Mini-package that contains modeling functions**
	- projected_traffic: Predicts aggregate AAWDT flow number for zip code over _N_ defined years, plots output

- **zip.show: Provides the user with an informational graphic on locations of numbered zip codes in the Seattle metro area.**
 
## 2. Predict how AAWDT flows by zip code will change in response to proposed urban planning efforts (increased sidewalks, more bike lanes, etc). ##

**Users: Citizens, policy makers, environmental groups, city planners**

Information provided by the user: Zip code of interest (map is visible to user), selected features, associated percent changes for each.

Response provided by the system: Predicted % increase in AAWDT within specified zip code for proposed additions. See sample below:


**Components and Sub-components:**
- **asdf: **
	- asdf: 	
- **asdf: **
	- asdf:
