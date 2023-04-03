##  Developer: Bartosz Tabisz

In the project I used the SQLite database in which the data is stored. In addition, during the execution of the tests, additional (constant) data is added so that the variability of the database does not affect the result of individual tests.

Below is an example of using the application:
### 1. Make a reservation
    Welcome to the tennis court booking app!
    What do you want to do:
    1) Make a reservation
    2) Cancel a reservation
    3) Print schedule
    4) Save schedule to a file
    5) Exit
    1

    Make a reservation
    What's your Name? (full name)
    Bartosz Tabisz

    When would you like to book? {DD.MM.YYYY HH:MM}
    25.03.2023 10:00

    The time you chose is unavailable, would you like to make a reservation for 10:30 (25.03.2023) instead? (Yes/No)
    No

    When would you like to book? {DD.MM.YYYY HH:MM}
    25.03.2023 14:00

    How long would you like to book court? (1/2/3/4)
    1) 30 minutes
    2) 60 minutes
    3) 90 minutes
    4) Back
    2

    Congratulations, court has been booked!
### 2. Cancel a reservation
    Cancel a reservation
    What's your Name? (full name)
    Bartosz Tabisz

    When would you like to cancel? {DD.MM.YYYY HH:MM}
    25.03.2023 14:00

    Your booking has been cancelled.
### 3. Print schedule
    Yesterday:
    * Edward Kowalski 16:00 - 17:30

    Today:
    No Reservations

    Tomorrow:
    No Reservations

    Saturday, 25. March 2023:
    * Max Ignaczak 10:00 - 10:30

### 4. Save schedule to a file
    Enter schedule start time? {DD.MM.YYYY}
    20.03.2023

    Enter schedule end time? {DD.MM.YYYY}
    25.03.2023

    Enter file name?
    file-name

    What format do you want to save the data in? (csv/json)
    json

    A .json file has been generated.
