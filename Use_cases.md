## Use Cases and Component Specifications of Traffic Model Predictor: ##


**1. Predict VER based on future Light-rail expansion routes**

User: Citizens, policy makers, environmental groups, city planners 

Information provided by the user: Region of construction for proposed light rail line, size of planned Light Rail expansion and expected reduction in vehicle traffic. 

Response provided by the system: Compares population-adjusted traffic flow data to that after user-input light rail information, computes VER for proposed light-rail expansion route, informs user if construction project is within bounds for expected reduction in vehicle traffic and displays maximum reduction
 
-Components:

Region of the city for proposed light rail expansion

	Sub component: printed menu of city regions

	Sub component: map visualization of city regions

Current year

Proposed length of light rail line

	Sub component: visualization of region choice

	Sub component: menu displaying mileage ranges for proposed installations

Expected reduction in vehicle traffic
 

**3. Provide general insight into predicted traffic patterns based on current trends**

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

