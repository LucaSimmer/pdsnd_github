import time
import pandas as pd
import numpy as np
from sys import exit

CITY_DATA = { 'chicago': 'chicago.csv',
              'new_york_city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = {0: 'all', 1:'january', 2:'february', 3:'march', 4:'april', 5:'may', 6:'june'}
DAYS = {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'saturday', 6:'sunday', 7:'all'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\nOBS: You can type "exit" to end program\n')
    while True:
        city = str(input('Choose between Chicago, New York City or Washington: ')).lower().strip().replace(' ', '_')
        if city == "exit": exit()
        if city in CITY_DATA: break
        print(f'You typed {city}')

    while True:
        month = str(input('Choose a month between january and june or all for no month filter: ')).lower()
        if month == "exit": exit()
        if month in MONTHS.values(): break
        print(f'You typed {month}')

    # get user input for month (all, january, february, ... , june)
    while True:
        day_of_week = str(input('Choose a day of the week between monday and sunday or all for no day filter: ')).lower()
        if day_of_week == "exit": exit()
        if day_of_week in DAYS.values(): break
        print(f'You typed {day_of_week}')

    # get user input for day of week (all, monday, tuesday, ... sunday)


    print('-'*40)
    return city, month, day_of_week


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

    df = pd.read_csv(f'{CITY_DATA[city]}', parse_dates=[1, 2])

    if month == 'all' and day == 'all': return df

    if month == 'all' and day != 'all':
        day = ''.join([str(k) for k, v in DAYS.items() if v == day])
        df = df[df['Start Time'].dt.dayofweek == int(day)]
        return df

    if month != 'all' and day == 'all':
        month = ''.join([str(k) for k, v in MONTHS.items() if v == month])
        df = df[df['Start Time'].dt.month == int(month)]
        return df

    if month != 'all' and day != 'all':
        day = ''.join([str(k) for k, v in DAYS.items() if v == day])
        month = ''.join([str(k) for k, v in MONTHS.items() if v == month])
        df = pd.DataFrame(df[(df['Start Time'].dt.month == int(month)) & (df['Start Time'].dt.dayofweek == int(day))])
        return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all' and day == 'all':
        freq_month = df['Start Time'].dt.month.value_counts()
        freq_hour = df['Start Time'].dt.hour.value_counts()
        print('List of months sorted by count of occurrences: ')
        for i in range(len(freq_month)): print(MONTHS[freq_month.index[i]].title() + ': ' + str(freq_month.iloc[i]))
        print(f'\nList of hour and count of occurrences for all months and all days are: ')
        for i in range(len(freq_hour)): print(str(freq_hour.index[i]) + ': ' + str(freq_hour.iloc[i]))

    # display the most common day of week
    if month != 'all' and day == 'all':
        freq_day = df['Start Time'].dt.dayofweek.value_counts()
        freq_hour = df['Start Time'].dt.hour.value_counts()
        print(f'List of day of week and count of occurrences for the month of {month.title()} are: ')
        for i in range(len(freq_day)): print(DAYS[freq_day.index[i]].title() + ': ' + str(freq_day.iloc[i]))
        print(f'\nList of hour and count of occurrences for the month of {month.title()} are: ')
        for i in range(len(freq_hour)): print(str(freq_hour.index[i]) + ': ' + str(freq_hour.iloc[i]))

    # display the most common start hour
    if month != 'all' and day != 'all':
        freq_hour = df['Start Time'].dt.hour.value_counts()
        print(f'List of hour and count of occurrences for the month of {month.title()} and on a {day.title()} are: ')
        for i in range(len(freq_hour)): print(str(freq_hour.index[i]) + ': ' + str(freq_hour.iloc[i]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\n\nList of the top 5 start stations by most popular:')
    for i in range(len(df['Start Station'].value_counts().head())):
        print(str(df['Start Station'].value_counts().head().index[i]) + ': ' + str(df['Start Station'].value_counts().head().iloc[i]))

    # display most commonly used end station
    print('\n\nList of the top 5 end stations by most popular:')
    for i in range(len(df['End Station'].value_counts().head())):
        print(str(df['End Station'].value_counts().head().index[i]) + ': ' + str(df['End Station'].value_counts().head().iloc[i]))


    # display most frequent combination of start station and end station trip
    print('\n\nTop 5 combination of start station and end station trip:')
    m_freq = df.groupby(['Start Station', 'End Station'], as_index=False).size().sort_values(by='size', ascending=False).head()
    for i in range(len(m_freq)): print(str(m_freq.iloc[i][0]) + ' + ' + str(m_freq.iloc[i][1]) + ': ' + str(m_freq.iloc[i][2]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time was: ' + str(df['Trip Duration'].sum()) + ' seconds')

    # display mean travel time
    print('Mean travel time was: ' + str(df['Trip Duration'].mean()) + ' seconds')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of user types')
    for i in range(len(df['User Type'].value_counts())):
        print(str(df['User Type'].value_counts().index[i]) + ': ' + str(df['User Type'].value_counts().iloc[i]))


    # Display counts of gender
    if city == 'chicago' or city == 'new_york_city' :
        print('\nCounts of gender:')
        for i in range(len(df['Gender'].value_counts())):
            print(str(df['Gender'].value_counts().index[i]) + ': ' + str(df['Gender'].value_counts().iloc[i]))

    # Display earliest, most recent, and most common year of birth
        temp = df.dropna(axis=0)
        print('\nEarliest year of birth: ')
        print(int(temp.sort_values(by='Birth Year').head(1).iloc[0 , -1]))
        print('\nMost recent, and most common year of birth: ')
        print(int(temp.sort_values(by='Birth Year').tail(1).iloc[0 , -1]))


        print('\nTop 5 most common year of birth:')
        for i in range(len(temp['Birth Year'].value_counts().head(5))):
            print(str(int(temp['Birth Year'].value_counts().head(5).index[i])) + ': ' + str(temp['Birth Year'].value_counts().head(5).iloc[i]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df, n, max_n):

    global flag
    flag = True

    if flag : print(df[int(n) : int(n) + 5])
    if n >= max_n:
        return print('You\'ve seen everything!')
    while flag:
        keep_going = str(input('\nWould you like to see more data? Enter yes or no.\n')).strip().lower()
        if keep_going == 'yes':
            n += 5
            print_raw_data(df, n, max_n)
        elif keep_going == 'no':
            flag = False
        elif keep_going == 'exit':
            exit()
        else:
            print('\nYou can answer only "yes", "no" or "exit"')
        continue

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        raw = str(input('\nWould you like to see the data? Enter yes or no.\n')).strip().lower()
        n = np.array(0)
        max_n = len(df)
        if raw == 'no': break
        elif raw == 'exit': exit()
        elif raw == 'yes': print_raw_data(df, n, max_n)

        while True:
            restart = str(input('\nWould you like to restart? Enter yes or no.\n')).strip().lower()
            if restart == 'yes': break
            elif restart == 'no': exit()
            elif restart == 'exit': exit()
            else:
                print('\nYou can answer only "yes", "no" or "exit"')
                continue


if __name__ == "__main__":
    main()
