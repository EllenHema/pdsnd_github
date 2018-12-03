import time
import pandas as pd
import numpy as np

#create datadictionary / data list reference for lateruse
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june','all']

days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see the data of Chicago, New York City or Washington?\n')
        city = city.lower()
        if city not in CITY_DATA.keys():
            print("We don't have the data of the city you typed in (or is it a typo?) Will restart to get correct input.\n")
        else:
            break

    #get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which Month do you want to filter the data on? Choice of January, February, March, April, May, June or All.\n')
        month = month.lower()
        if month not in months:
            print("We don't have the data of the month you typed in (or is it a typo?) Will restart to get correct input. ")
        else:
            break
    #get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day of week do you want to filter the data on? Choice of Monday ~ Sunday or All.\n')
        day = day.lower()
        if day not in days:
            print("We don't have the data of the day of week you typed in (or is it a typo?) Will restart to get correct input. ")
        else:
            break

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

     # filter by month if applicable

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df2 = df[df['month'] == month]
    else:
        df2 = df
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df3 = df2[df2['day_of_week'] == day.title()]
    else:
        df3 = df2

    df = df3

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    start_time = time.time()
    print('\nCalculating The Most Frequent Times of Travel...\n')

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    #display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_dayofweek = df['day_of_week'].mode()[0]
    print('Most Popular day of week:', popular_dayofweek)
    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    start_station = df['Start Station'].value_counts()
    print('The most popular start station is: {}, chosen {} times.'.format(start_station.index[0],start_station[0]))

    #display most commonly used end station
    end_station = df['End Station'].value_counts()
    print('The most popular end station is: {}, chosen {} times.'.format(end_station.index[0],end_station[0]))

    #display most frequent combination of start station and end station trip
    df['Combine_start_end'] = df['Start Station'] + ' and ' + df['End Station']
    Combine_start_end = df['Combine_start_end'].value_counts()
    print('The most popular start and end station combination is: {}, chosen {} times.'.format(Combine_start_end.index[0],Combine_start_end[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_duration = df['Trip Duration'].sum()/60
    print('The total travel time is {} min(s) or {} hour(s).'.format(round(total_duration,2), round(total_duration/60,2)))
    #display mean travel time
    avg_duration = df['Trip Duration'].mean()/60
    print('The average travel time is {} min(s) or {} hour(s).'.format(round(avg_duration,2), round(avg_duration/60,2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe breakdown of user types are:\n', user_types)

    if 'Birth Year' not in df.columns or 'Gender' not in df.columns:
        print('Sorry, the dataset does not have Gender or Birth Year data available.')
    else:
        #Display counts of gender
        gender = df['Gender'].value_counts()
        print('\nThe breakdown of genders are:\n',gender)

        #Display earliest, most recent, and most common year of birth
        early_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].value_counts()
        print('The earliest birth year among users is: {}, the most recent one is: {}, the most common birth year is: {}, which appears {} times.'.format(int(early_birth), int(recent_birth), int(common_birth.index[0]), common_birth.iloc[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# print five columns of data if selected and keep printing next five if asked
def pfive(indv_data,df):
    if indv_data.lower() == 'yes':
        print(df[:5])
        df1=df.iloc[5:len(df),]
        indv_data1 = input('\nWould you like to see 5 more individual data? Enter yes or no.\n')
        if len(df1)<5:
            print('No more than 5 data to show!')
        else:
            pfive(indv_data1,df1)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        indv_data = input('\nWould you like to see 5 individual data? Enter yes or no.\n')
        pfive(indv_data,df)


        # Get restart / not request
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
