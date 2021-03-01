import time
import math
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = { 'january': 1,
                'february': 2,
                'march': 3,
                'april': 4,
                'may': 5,
                'june': 6,
                'jan': 1,
                'feb': 2,
                'mar': 3,
                'apr': 4,
                'may': 5,
                'jun': 6}

WEEK_DATA = { 'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6,
                'mon': 0,
                'tues': 1,
                'wed': 2,
                'thur': 3,
                'fri': 4,
                'sat': 5,
                'sun': 6}

def get_filters():
    """
    Prompts user to provide a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    print()
    # TO DO: get the user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while 1:
        print('Which city\'s data do you want?')
        chosencity = input('Type Chicago or CH for Chicago, New York City or NYC for New York, and Washington or WA for Washington DC \n').lower()
        print()
        if chosencity=='ch' or chosencity=='chicago':
            chosencity='chicago'
        if chosencity=='ny' or chosencity=='nyc':
            chosencity='new york city'
        if chosencity=='wa' or chosencity=='washington' or chosencity=='washington dc':
            chosencity='washington'
        if chosencity not in CITY_DATA:
            print('Kindly enter a valid city \n')
            continue
        chosencity = CITY_DATA[chosencity]
        break
    # TO DO: get the user input for month (all, january, february, ... , june)
    # TO DO: get the user input for day of week (all, monday, tuesday, ... sunday)
    while 1:
        duration = input('Do you want to filter the data by month and/or week? Type Yes/No or y/n \n').lower()
        print()
        if duration=='yes' or duration=='y' or duration=='yap':
            duration=True
        elif duration=='no' or duration=='n' or duration=='nope':
            duration=False
        else:
            print('You did not enter a valid duration. Please try again. \n')
            continue
        break

    while 1:
        if duration:
            filter=input('Filter by month / day or both. Type month for month, day for day \n').lower()
            print()
            if filter=='month':
                print('Which month\'s data do you want?')
                month = input('January/jan, February/feb, March/mar, April/apr, May, June/jun- \n').lower()
                print()
                if month not in MONTH_DATA:
                    print('Sorry I did not understand that input. Could you try again?')
                    continue
                month = MONTH_DATA[month]
                day='all'
            elif filter=='day':
                print('Which day\'s data  do you want? ')
                day = input('Monday/mon, Tuesday/tues, Wednesday/wed, Thursday/thur, Friday/fri, Saturday/sat, Sunday/sun- ').lower()
                print()
                if day not in WEEK_DATA:
                    print('Sorry I did not understand that input. Could you try again?\n')
                    continue
                day = WEEK_DATA[day]
                month='all'
            elif filter=='both':
                print('Which month\'s data  do you want?')
                month = input('January/jan, February/feb, March/mar, April/apr, May, June/jun- ').lower()
                print()
                if month not in MONTH_DATA:
                    print('Sorry I did not understand that input. Could you try again?')
                    continue
                month = MONTH_DATA[month]
                print('And day of the week?')
                day = input('Monday/mon, Tuesday/tues, Wednesday/wed, Thursday/thur, Friday/fri, Saturday/sat, Sunday/sun- ').lower()
                print()
                if day not in WEEK_DATA:
                    print('Sorry I did not understand that input. Could you try again?')
                    continue
                day = WEEK_DATA[day]
            else:
                print('Sorry I did not understand that input. Could you try again?')
                continue
            break
        else:
            day='all'
            month='all'
            break

    print('-'*40)
    return chosencity, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    df = pd.read_csv(city)
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    if day != 'all':
        df = df[df['day_of_week'] == day]
    if month != 'all':
        df = df[df['month'] == month]
    df.drop('day_of_week',axis=1,inplace=True)
    df.drop('month',axis=1,inplace=True)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    #temporary_df = pd.read_csv(city)
    # TO DO: display the most common month
    most_freq_month = df['month'].mode()[0]
    for num in MONTH_DATA:
        if MONTH_DATA[num]==most_freq_month:
            most_freq_month = num.title()
    print('The most common month for travel is {}'.format(most_freq_month))

    # TO DO: display the most common day of week
    most_freq_day = df['day_of_week'].mode()[0]
    for num in WEEK_DATA:
        if WEEK_DATA[num]==most_freq_day:
            most_freq_day = num.title()
    print('The most common day of week for travel is {}'.format(most_freq_day))

    # TO DO: display the most common start hour
    df['hour']=pd.to_datetime(df['Start Time']).dt.hour
    most_freq_hour = df['hour'].mode()[0]
    print('The most common hour for travel is {}'.format(most_freq_hour))
    df.drop('hour',axis=1,inplace=True)
    df.drop('day_of_week',axis=1,inplace=True)
    df.drop('month',axis=1,inplace=True)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Display the statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: This displays the most commonly used start station
    print()
    print('Most commonly used start station as per our data was {}'.format(df['Start Station'].mode()[0]))

    # TO DO: This result displays the most commonly used end station
    print()
    print('Most commonly used end station as per our data was {}'.format(df['End Station'].mode()[0]))

    # TO DO: This code displays the most frequent combination of start station and end station trip
    print()
    most_freq_station_comb = df['Start Station'] + ' to ' + df['End Station']
    print('The most frequent combination of start station and end station trip was {}'.format(most_freq_station_comb.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays stats on the total and average trip duration.
    """

    print('\n Calculating Trip Duration...\n')
    start_time = time.time()
    travel_durations = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])

    # TO DO: This displays total travel time
    print()
    td_sum = df['Trip Duration'].sum()
    sum_seconds = td_sum%60
    sum_minutes = td_sum//60%60
    sum_hours = td_sum//3600%60
    sum_days = td_sum//24//3600
    print('Passengers travelled a total of {} days, {} hours, {} minutes and {} seconds'.format(sum_days, sum_hours, sum_minutes, sum_seconds))

    # TO DO: This displays mean travel time
    print()
    td_mean = math.ceil(df['Trip Duration'].mean())
    mean_seconds = td_mean%60
    mean_minutes = td_mean//60%60
    mean_hours = td_mean//3600%60
    mean_days = td_mean//24//3600
    print('Passengers travelled an average of {} hours, {} minutes and {} seconds'.format(mean_hours, mean_minutes, mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    
    """

    print('\n Calculating User Stats...\n')
    start_time = time.time()

    # TO DO: This code Display the counts of user types
    print()
    types_of_users = df.groupby('User Type',as_index=False).count()
    print('Number of types of users are {}'.format(len(types_of_users)))
    for i in range(len(types_of_users)):
        print('{}s - {}'.format(types_of_users['User Type'][i], types_of_users['Start Time'][i]))

    # TO DO: This Displays counts of gender
    print()
    if 'Gender' not in df:
        print('Shoot, no gender data for this city ')
    else:
        gender_of_users = df.groupby('Gender',as_index=False).count()
        print('Number of genders of users mentioned in the data are {}'.format(len(gender_of_users)))
        for i in range(len(gender_of_users)):
            print('{}s - {}'.format(gender_of_users['Gender'][i], gender_of_users['Start Time'][i]))
        print('Gender data for {} users is not available.'.format(len(df)-gender_of_users['Start Time'][0]-gender_of_users['Start Time'][1]))

    # TO DO: This displays the earliest, most recent, and most common year of birth
    print()
    if 'Birth Year' not in df:
        print('Data related to birth year of users is not available for this city.')
    else:
        birth = df.groupby('Birth Year', as_index=False).count()
        print('Earliest year of birth was {}.'.format(int(birth['Birth Year'].min())))
        print('Most recent year of birth was {}.'.format(int(birth['Birth Year'].max())))
        print('Most common year of birth year was {}.'.format(int(birth.iloc[birth['Start Time'].idxmax()]['Birth Year'])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_rawdata(df):
    """
    Takes user input to decide whether to display a set of 5 raw data

    """
    wantrawdata = input('Would you like to read some of the raw data? Yes/No \n').lower()
    print()
    if wantrawdata=='yes' or wantrawdata=='y' or wantrawdata=='yeah':
        wantrawdata=True
    elif wantrawdata=='no' or wantrawdata=='n' or wantrawdata=='nope':
        wantrawdata=False
    else:
        print('You did not enter a valid answer. Let\'s try that again. \n')
        display_rawdata(df)
        return

    if wantrawdata:
        a = 0
        while 1:
            for i in range(a, a+5):
                print(df.iloc[i])
                #print(i)
            a+=5
            wantrawdata = input('Another five? Yes/No ').lower()
            if wantrawdata=='yes' or wantrawdata=='y' or wantrawdata=='yeah':
                continue
            elif wantrawdata=='no' or wantrawdata=='n' or wantrawdata=='nope':
                break
            else:
                print('You did not enter a valid answer.')
                return

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_rawdata(df)

        restart = input('\nWould you like to restart and try again? Enter yes or no.\n').lower()
        print()
        if restart == 'no' or restart == 'n' or restart == 'yap':
            break

if __name__ == "__main__":
	main()