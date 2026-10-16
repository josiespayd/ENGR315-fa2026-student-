import sys

"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###

## Filter function to analyze the data for a specific county and state
def analyze_location(data, county_name, state_name):
    filtered_data = []
    for entry in data:
        if entry[1] == county_name and entry[2] == state_name:
            filtered_data.append(entry)

    if len(filtered_data) == 0:
        print(f"No data found for {county_name}, {state_name}.")
        return None

## Finding Dates and cumulative cases for the filtered data
    dates = []
    cumulative_cases = []
    for entry in filtered_data:
        dates.append(entry[0])
        cumulative_cases.append(entry[4])

    # Question 1: first date with reported cases
    first_date = dates[0]
    for i in range(len(dates)):
        if cumulative_cases[i] > 0:
            first_date = dates[i]
            break

    # Question 2: calculate daily new cases and find the maximum single-day increase
    daily_new_cases = [0]
    for i in range(1, len(cumulative_cases)):
        diff = cumulative_cases[i] - cumulative_cases[i - 1]
        if diff < 0:
            diff = 0
        daily_new_cases.append(diff)

    max_single_day_cases = max(daily_new_cases)
    max_single_day_date = dates[daily_new_cases.index(max_single_day_cases)]

    # Question 3: find the maximum seven-day total
    max_seven_day_sum = -1
    max_seven_day_start_date = ''
    max_seven_day_end_date = ''

    for i in range(len(daily_new_cases) - 6):
        seven_day_sum = sum(daily_new_cases[i:i + 7])
        if seven_day_sum > max_seven_day_sum:
            max_seven_day_sum = seven_day_sum
            max_seven_day_start_date = dates[i]
            max_seven_day_end_date = dates[i + 6]

    # Output the results
    print("Results for " + county_name + "," + state_name + ":")
    print("First date with reported cases: " + first_date)
    print("Maximum single-day new cases: " + str(max_single_day_cases) + " on " + max_single_day_date)
    print("Maximum seven-day sum: " + str(max_seven_day_sum) + " from " + max_seven_day_start_date + " to " + max_seven_day_end_date)
    print("Total cumulative cases: " + str(cumulative_cases[-1]))
    print()


if __name__ == "__main__":
    # File path
    file_path = "data/covid/us-counties.csv"

    # Dataset
    data = parse_nyt_data(file_path)

    # Analyze data for a specific county and state
    analyze_location(data, "Harrisonburg city", "Virginia")
    analyze_location(data, "Rockingham", "Virginia")

