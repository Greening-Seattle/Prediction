## Use Cases and Component Specifications of Traffic Model Predictor: ##


## 1. Predict future traffic flows by zip code: ##

**Users: Citizens, policy makers, environmental groups, city planners** 

Information provided by the user: Zip code of interest (map is visible to user), future year to predict traffic flow. 

Response provided by the system: Projected percent increase in traffic flow for a given year based on historical data within the specified zip code.
 
**Components:**
1. zip.show() -- provides the user with an informational graphic on locations of numbered zip codes in the Seattle metro area.
2. 
 
## 2. Provide general insight into predicted traffic patterns based on current trends ##

User: Citizens, contractors, city planners, restaurant/business owners
Information provided by the user: New or existing building, region of Seattle, address for isolating local traffic flow
Response provided by the system: Predicted % increase in traffic volumes in the future for that specific region and street
 
Components:

Existing building or new construction project

Region of the city for proposed project (if new construction)

	Sub component: printed menu of city regions

	Sub component: map visualization of city regions

Proposed start date for construction (if new construction)

	Sub-component: Season (Summer/Fall/Winter/Spring)

	Sub-component: Year

Proposed end date for construction (if new construction)

	Sub-component: Season (Summer/Fall/Winter/Spring)

	Sub-component: Year

Address

