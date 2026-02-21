Airline Flight Delay & Operations Database Course Project

Application Domain:
My project simulates a database that tracks airline operations using 2015 flight data to help identify the main causes of airline delays during that time.

Project Scope:
- Flight schedules
- Scheduled and actual departure times
- Scheduled and actual arrival times
- Delay events and associated root causes
- Airline information
- Airport information
- Weather data and time records will help identify the primary causes of flight delays and  valuate airline performance.

Users:
- Airline operators who monitor flight performance (SLA compliance)
- Regulatory and security systems for record keeping
- Airline companies for performance improvement
- Data analysts studying delay trends and root causes

Data Source:
2015 Flight Delays and Cancellations Dataset
https://www.kaggle.com/datasets/usdot/flight-delays?select=flights.csv

Entities:
- Airline
- Airport
- Flight
- Delay (weak entity dependent on Flight)
- Airline_Airport (associative entity resolving many-to-many relationship)


Relationships:
One-to-many:
- Multiple flights can belong to the same airline.
- One flight can have multiple delay records.

Many-to-many:
- An airport can have many airlines.
- An airline can operate at many airports.
  (This relationship is resolved using the Airline_Airport associative entity.)

Role-based relationship:
- One flight departs from one airport and arrives at one airport.
