# Bike Share Project
import pandas as pd
import numpy as np
import time

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}

def get_city():
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_aliases = {'ny': 'new york city','new york': 'new york city', 'nyc': 'new york city'} #New York could be shortened - ny, nyc
    while True:
        city = input("What city would you like to see? Chicago, Washington or New York City? ").lower().strip() #lowercase to account for capitalization and account for whitespace
        city = city_aliases.get(city, city)
        if city in CITY_DATA.keys():
            print(f"Selected City: {city.title()}") #capitalization of the first letter
            return city
        print("Oops - please correct your spelling. Enter Washington, Chicago or New York.")

def get_filter():
    # Ask the user what types of filters they want to use
    correct_filters = ['month', 'day', 'both', 'none'] #reference for input
    while True:
        filter_input = input("Would you like to filter by month, day, both or none? ").lower().strip() #lowercase, removes white space
        if filter_input in correct_filters:
            print(f"Selected filter: {filter_input}")
            return filter_input
        print("The selection invalid - please enter month, day, both, or none.")

def get_month():
  # TO DO: get user input for month (all, january, february, ... , june)
    correct_months = ['january', 'february', 'march', 'april', 'may', 'june']
    
    while True:
        month = input("Which month would you like to see? (January, February, March, April, May, June) ").lower().strip() #lowercase to account for capitalization and account for whitespace
        if month in correct_months:
            print(f"Selected month: {month.title()}") #capitalization of the first letter
            return month
        print("Selection invalid - please enter January, February, March, April, May, June.")

def get_day():
   # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    correct_days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'] 
    
    while True:
        day = input("Which day would you like to see? Please enter Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or Saturday ").lower().strip() #lowercase to account for capitalization and account for whitespace
        if day in correct_days:
            print(f"Selected day: {day.title()}") #capitalization of the first letter
            return day
        print("The selection is invalid - please enter Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or Saturday.") 

def get_filters():
    """
    collects:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    while True:
        print("Hello! Let's explore some US bikeshare data!")
        
    # inputs 
        city = get_city() #first input needed
        filter_input = get_filter() #prompt filter type
        month = 'all' #no month filter unless prompted for override, ex "none"
        day = 'all' #no day filter unless prompted, ex "none"
        if filter_input == 'month':
            month = get_month()
        elif filter_input == 'day':
            day = get_day()
        elif filter_input == 'both': #prompt for both
            month = get_month()
            day = get_day()
        
    # Summary selection
        print(f"\nYou selected {city.title()} and {filter_input}") #selected city and filters
        if month != 'all':
            print(f"Month: {month.title()}") #show the month for filter
        else:
            print("Month: none")
        if day != 'all':
            print(f"Day: {day.title()}") #day when a filter is applied
        else:
            print("Day: none")
        
    # Ask to confirm or restart the prompt
        confirm = input("\nDo these selections work? (yes/no)").lower().strip()
        if confirm in ['yes', 'y']:
            break
        print("Ok, let us start over\n")
    
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month != 'all':
        df = df[df['Start Time'].dt.month_name().str.lower() == month]
    if day != 'all':
        df = df[df['Start Time'].dt.day_name().str.lower() == day]
        
    return df

    #Display 5 rows of data to continue on
def display_data(df):
    i = 0 
    while True:
        print(df.iloc[i:i+5]) #sets 5 rows
        if input("\n Would you like to see 5 more rows? (yes/no) ").lower().strip() not in ['y', 'yes']: #if no, it stops
            break
        i += 5

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

#Display most common month, day, hour
    if not df.empty:
        month_common = df['Start Time'].dt.month_name().mode()[0] #shows first mode
        print(f"Most common month: {month_common}")
    else:
        print("No data for most common months")

    if not df.empty:
        day_common = df['Start Time'].dt.day_name().mode()[0] #shows first mode
        print(f"Most common day: {day_common}")
    else:
        print("No data for most common day")

    if not df.empty:
        hour_common = df['Start Time'].dt.hour.value_counts().idxmax()
        hours = f"{hour_common:00}" #two digits
        print(f"Most common hour: {hours}")
    else:
        print("No data for most common hour")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if not df.empty:
        common_start_station = df['Start Station'].mode()[0] #first mode
        print(f"Most commonly used start station: {common_start_station}")
    else: 
        print("No data for most commonly used start station")

    if not df.empty:
        common_end_station = df['End Station'].mode()[0] #first mode
        print(f"Most commonly used end station: {common_end_station}")
    else: 
        print("No data for most commonly used end station")

    if not df.empty:
        df['trip'] = df['Start Station'] + ' to ' + df['End Station'] #combine to create frequent trip
        trip = df['trip'].value_counts().idxmax() #frequent trip
        start_station, end_station = trip.split(' to ', 1)
        print(f"Most frequent trip: from {start_station} to {end_station}")
        df = df.drop('trip', axis=1) #drop column, not row
    else:
        print("No data available for most frequent trips.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return df

def trip_duration_stats(df):
#Displays statistics on the total and average trip duration.
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
#Travel time minutes
    if not df.empty:
        total_travel_minutes = df['Trip Duration'].sum() / 60 #minutes
        print(f"Total travel time: {total_travel_minutes:.2f} minutes") #decimals
    else:
        print("No data for total travel time")
        
#Travel time hours
    if not df.empty:
        total_travel_hours = df['Trip Duration'].sum() / 3600 #hours
        print(f"Total travel time: {total_travel_hours:.2f} hours") #decimals
    else:
        print("No data for total travel time")
        
#Travel time mean/minutes
    if not df.empty:
        mean_trip_duration = df['Trip Duration'].mean() / 60 #minutes
        print(f"Mean travel time: {mean_trip_duration:.2f} minutes") #decimals
    else:
        print("No mean data is available.")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if not df.empty and 'User Type' in df.columns and df['User Type'].notna().any(): # last part for missing values
        user_type = df['User Type'].value_counts()
        print("User type count: ")
        print(user_type)
    else:
        print("\n No data for user counts.")

    # TO DO: Display counts of gender
    if not df.empty and 'Gender' in df.columns and df['Gender'].notna().any(): #last part for missing values
        gender_total = df['Gender'].value_counts()
        print("\nCount of gender: ")
        print(gender_total)
    else:
        print("\n No data for gender.")

   # TO DO: Display earliest, most recent, and most common year of birth
    if not df.empty and 'Birth Year' in df.columns and df['Birth Year'].notna().any(): #last part for missing values
        birth_year = df['Birth Year'].dropna().astype(int) #needed for casting as integer so the birth year is not YYYY.0
        earliest_year_of_birth = birth_year.min() #integer data type, smallest
        recent_year_of_birth = birth_year.max() #integer data type, largest
        common_year_of_birth = birth_year.mode()[0] #integer data type - common
        print(f"\nEarliest year of birth: {earliest_year_of_birth}")
        print(f"\nMost recent year of birth: {recent_year_of_birth}")
        print(f"\nMost common year of birth: {common_year_of_birth}")
    else:
        print("\nNo data for birth year.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        df = station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df) #needed for the 5 row prompt

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()

#Note for improvement - add a final greeting when the user enters 'no' for "would you like to restart?"