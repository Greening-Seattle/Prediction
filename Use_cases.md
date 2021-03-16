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

- **zip.show: Provides the user with an informational graphic on locations of numbered zip codes in the Seattle metro area.
 
## 2. Provide general insight into predicted traffic patterns based on current trends ##

User: Citizens, contractors, city planners, restaurant/business owners
Information provided by the user: New or existing building, region of Seattle, address for isolating local traffic flow
Response provided by the system: Predicted % increase in traffic volumes in the future for that specific region and stree
