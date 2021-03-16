## Use Cases and Component Specifications of Traffic Model Predictor ##


## 1. Predict future traffic volumes by zip code. ##

**Users: Citizens, policy makers, environmental groups, city planners** 

_Information provided by the user:_ Zip code of interest (map is visible to user), future year to predict AAWDT (Annual Average Weekday Traffic) flow. 

_Response provided by the system:_ Projected percent increase AAWDT for a given year based on historical data within the specified zip code.
 
**Components and Sub-components:**
- **greendata: Mini-package that regulates all traffic data downloads from Seattle.gov for processing**
	- get_alltraffic: Compiles all AAWDT data from 2007 - 2018 for use, no user input
- **greenseattle: Mini-package that contains traffic projections, artificial NN modeling functions and associated outputs**
	- projected_traffic: Predicts aggregate AAWDT flow number for zip code over user-input _N_ years

- **zip.show: Provides the user with an informational graphic on locations of numbered zip codes in the Seattle metro area.**
 
## 2. Predict how AAWDT flows by zip code will change in response to proposed urban planning efforts (increased sidewalks, more bike lanes, etc). ##

**Users: Citizens, policy makers, environmental groups, city planners**

_Information provided by the user:_ Zip code of interest (map is visible to user), selected features, associated percent changes for each.

_Response provided by the system:_ Predicted % increase in AAWDT within specified zip code for proposed additions.


**Components and Sub-components:**
- **greendata: Mini-package that contains traffic projections, artificial NN modeling functions and associated outputs**
	- get_csv_alldata: Downloads all compiled data (across all zip codes, years and input features), no user input
- **greenseattle: Mini-package that contains modeling functions**
	- prepare_nn: Trains artificial neural network on all geospatial-time data, normalized to mean values of each feature with hyperbolic tan activation func
	- model_viz: Executes model output for artificial NN based on user input of zipcode
		- feature_proction: Executes the model for use within model_viz
