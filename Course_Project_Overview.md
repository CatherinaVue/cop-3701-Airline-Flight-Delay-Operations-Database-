Airline Flight Delay & Operations Database Course Project

Application Domain: My project simulates the database tracking operations of airlines as data from 2015 will be used to help identify the main causes for an airline's delay during this time.

Project Scope: 
My database will store details of flight schedules, scheduled and actual departure and arrival times, delay events, and associated root causes. Weather data and time records will help identify the main causes for delay.

Users:
- Airline operators who monitor flight performance (SLA)
- Regulatory/security systems for records
- airline companies for performance improvement

Data Sources: 2015 Flight Delays and Cancellations - https://www.kaggle.com/datasets/usdot/flight-delays?select=flights.csv

Entities: 
- Flights (string)
- Delays (weak depends on flight)
- Airline (strong)
- Airport (strong)
- Airline_Airport (bridge - associative entity)

Attributes:
- Identifier attributes: FlightID, AirlineID, AirportID
- Mandatory attribute example: FlightNumber (must exist for every flight)
- Optional attribute example: GateNumber (may not always be assigned)
- Single-value attribute example: ScheduledDepartureTime

Relationships: 

One-to-One:
- One Flight departs from one Airport and arrives at one Airport

One-to-Many:
- One Airline can operate many Flights.
- One Flight can have multiple Delay records.

Many-to-many: 
- An airport can have many airlines and an airline can operate at many airports.
- One-to-one: One flight will depart at one airport to another one
