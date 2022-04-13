import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv','new york': 'new_york_city.csv','washington': 'washington.csv' }

def user_input_check(in_str, in_type):
    """
    check for user input to ensure city, month, day are entered rigth and not allaw any error because of typos

    arg:
    in_str: the string appeared for the user 
    in_type: city or month or day

    return
    the right input from user (in_store)
    """
    while True:
        in_store = input(in_str).lower()
        try:
            if in_store in ["chicago","new york","washington" ] and in_type =="city":
                break
            elif in_store in ["all", "january","february","march","april","may","june"] and in_type == "month":
                break
            elif in_store in ["all","monday","tuesday","wednesday","thursday","friday","saturday","sunday"] and in_type == "day":
                break
            elif in_store in ["yes","no"] and in_type == "answer":
                break
            else:
                print("wrong Entry try again!")

        except ValueError:
            print("wrong Entry try again!")
    return in_store
            


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = user_input_check("Would you like to see data for Chicago, New York, or Washington? Enter the city you want: ","city")
    # get user input for month (all, january, february, ... , june)t

    month = user_input_check("Would you like to filter the data by month?Enter the month you want if you want all months write all: ","month")
    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = user_input_check("Would you like to filter the data by day? Enter the day you want if you want all days write all : ","day")
    print('Hello! Let\'s explore some US bikeshare data!')

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
    df = pd.read_csv(CITY_DATA[city])
    #print("df1",df)#debugging 
    #convert start time column to datetime
    df['Start Time']= pd.to_datetime(df['Start Time'])
    #print("df2",df)#debugging
    #assign values of month , day, hour from start time and create column for each of them
    df['month']= df['Start Time'].dt.month
    #print("df3",df)#debugging
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #print("df4",df)#debugging
    df['hour'] = df['Start Time'].dt.hour
    #filter by month if value entered by user not all
    if month != "all":
        months = ["january","february","march","april","may","june"]
        month = months.index(month) + 1
        #filter by month to create filtered dataframe
        df = df[df['month'] == month]
        #print("df5",df)#debugging

        
    #filter by day of week if value entered by user not all
    if day !="all":
        df= df[df['day_of_week'] == day.title()]
        #print("df6",df)#debugging

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print(type(df))
    #print(df)

    # display the most common month
    months = ["January","February","March","April","May","June"]
    month= df['month'].mode()[0]
    print("the most common month is: {}".format(months[month-1]))
    


    # display the most common day of week
    days = ["all","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    day = df['day_of_week'].mode()[0]
    print("the most common day is: {}".format(day))
   


    # display the most common start hour
    print("the most common hour is : ", df['hour'].mode()[0])
    


    print("\nThis took %s seconds."  % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Common_Start = df['Start Station'].mode()[0]

    print("the most common start station is: ", Common_Start)



    # display most commonly used end station
    print("the most common End station is: ", df['End Station'].mode()[0])



    # display most frequent combination of start station and end station trip
    start_end = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print("most common trip from start to end: ", start_end)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    print("total travel time is: ", df['Trip Duration'].sum())

    print('\nCalculating mean travel time...\n')
    # display mean travel time
    print("average travel time is: ", df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("user types are as follow", df['User Type'].value_counts())


    # Display counts of gender
    if city != 'washington':
        print("Gender types are as follow: ", df['Gender'].value_counts())
        # Display earliest, most recent, and most common year of birth
        print("the most common year of Birth is: ", int(df['Birth Year'].mode()[0]))
        print("the earliest year of birth is: ",  int(df['Birth Year'].min()))
        print("the recent year of birth is: ", int(df['Birth Year'].min()))




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def ask_user (df):
    """prompt to ask user if he want to display the raw data and iterating in data 5 by 5 rows

    Arg:
    df: filtered/selected dataframe

    return none

    
    """
    print('\nprompt for displaying raw data...\n')
    start_time = time.time()
        # ask user for input and call check input for avoiding typo or value error
    in_user = user_input_check("Do you want to view first 5 rows of data? yes/ or no: ", "answer")
    i_start = 0

    #iterating in dataframe 5by 5 rows according to user answer
    while True:
        if in_user == "no":
            break
        print(df.iloc[i_start:i_start+5])
        i_start += 5
        ask_another = user_input_check("Do you want to view Next 5 rows of data? yes/ or no: ", "answer")
        if ask_another == "no":
            break
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
        

        
        


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        #print("df",  df)#debugging
        ask_user(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
