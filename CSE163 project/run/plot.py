"""
This python module will create some new dataframes: inew_df, wa_df and state_df
each of which is useful for our visualization, mapping and machine learning
in this program. This module also creates some visualization plots (like
histogram, line chart, and scatter plot) to examine some potential factor's
flight delays' distribution. So the readers can easily understand if some
factors are influencial to flight delays.
"""

# Import modules and functions for csv files and plotting.
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns


class plot():
    def __init__(self, wa_df):
        """
        Implement an initializer for the class ML_Model.
        It takes in a data set and a string describing the size of the dataset.
        """
        self._wa_df = wa_df

    # Visualization examples
    def total_flights(self):
        """
        It takes the WA dataframe and plots a bar chart that compares the
        number of flights from Washington State to any other states in the US.
        The graph will be saved as 'flights_per_state.png'.
        """
        plt.figure(figsize=(13.5, 7))
        sns.histplot(data=self._wa_df, x='STATE')
        plt.xticks(rotation=-55)
        plt.title('The Total Number of Flights to each States from WA')
        plt.xlabel('Arriving States')
        plt.ylabel('Number of Flights')
        plt.savefig('flights_per_state.png', bbox_inches='tight')

    def delay_ratio_time_distance(self):
        """
        It takes the WA dataframe and produces a scatter plot that examines
        whether the "delay time & distance ratio" is
        strongly-positively-related to the "delay time & standard flight time
        ratio". The graph will be saved as 'distance_to_flightTime.png'.
        """
        sns.relplot(x='DELAY_RATIO_DISTANCE', y='DELAY_RATIO_TIME',
                    data=self._wa_df, color='r')
        # Limits the x-axis and y-axis to the same range.
        plt.xlim([-3, 25])
        plt.ylim([-3, 25])
        plt.title('Correlation between "Distance Ratio" and "Duration Ratio')
        plt.xlabel('Flight Delay Ratio based on Flight Distance')
        plt.ylabel('Flight Delay Ratio based on Planned Flight Duration')
        plt.savefig('distance_to_flightTime.png', bbox_inches='tight')

    def airlines_delay(self):
        """
        It takes the WA dataframe and produces a sorted histogram which shows
        the airlines from the highest to lowest average delay-time-ratio. The
        graph will be saved as 'delay_per_airlines.png'.
        """
        airline_s =\
            self._wa_df.groupby('ABBR_AIRLINE')['DELAY_RATIO_TIME'].mean()
        # Sorts the airlines descendingly based on values in
        # 'DELAY_RATIO_TIME'.
        airline_s = airline_s.sort_values(ascending=False)
        plt.figure(figsize=(7, 7))
        sns.barplot(x=airline_s.index, y=airline_s.values, color='0.6')
        plt.title('Average Arrival Delays by Airlines')
        plt.xlabel('Airlines (2-letters)')
        plt.ylabel('Delays (duration ratio)')
        plt.savefig('delay_per_airlines.png', bbox_inches='tight')

    def states_delay(self):
        """
        It takes the WA dataframe and produces a sorted histogram which shows
        the arriving states from the highest to lowest average
        delay-time-ratio, and the color of the bars represents which region
        the state is in. Also, it returns a dataframe called state_df that
        added the 'REGION' column. The graph will be saved as
        'delay_per_states.png'.
        """
        state_s = self._wa_df.groupby('STATE')['DELAY_RATIO_TIME'].mean()
        state_df = pd.DataFrame({'STATE': state_s.index,
                                'MEAN_DELAY': state_s.values})
        # Classify each states into one of the four regions based on where it
        # is located by creating a categorical column 'REGION'.
        northwest = (state_df['STATE'] == 'WA') |\
            (state_df['STATE'] == 'OR') |\
            (state_df['STATE'] == 'ID') | (state_df['STATE'] == 'MT') |\
            (state_df['STATE'] == 'WY') | (state_df['STATE'] == 'ND') |\
            (state_df['STATE'] == 'SD') | (state_df['STATE'] == 'NE') |\
            (state_df['STATE'] == 'MN') | (state_df['STATE'] == 'IA') |\
            (state_df['STATE'] == 'WI') | (state_df['STATE'] == 'IL') |\
            (state_df['STATE'] == 'UT') | (state_df['STATE'] == 'CO') |\
            (state_df['STATE'] == 'KS') | (state_df['STATE'] == 'MO') |\
            (state_df['STATE'] == 'AK')
        southwest = (state_df['STATE'] == 'CA') |\
            (state_df['STATE'] == 'NV') |\
            (state_df['STATE'] == 'AZ') | (state_df['STATE'] == 'NM') |\
            (state_df['STATE'] == 'TX') | (state_df['STATE'] == 'OK') |\
            (state_df['STATE'] == 'AR') | (state_df['STATE'] == 'LA') |\
            (state_df['STATE'] == 'HI')
        southeast = (state_df['STATE'] == 'MS') |\
            (state_df['STATE'] == 'AL') |\
            (state_df['STATE'] == 'GA') | (state_df['STATE'] == 'FL') |\
            (state_df['STATE'] == 'SC') | (state_df['STATE'] == 'NC') |\
            (state_df['STATE'] == 'TN') | (state_df['STATE'] == 'KY') |\
            (state_df['STATE'] == 'WV') | (state_df['STATE'] == 'VA')
        northeast = (state_df['STATE'] == 'MI') |\
            (state_df['STATE'] == 'IN') |\
            (state_df['STATE'] == 'OH') | (state_df['STATE'] == 'PA') |\
            (state_df['STATE'] == 'MD') | (state_df['STATE'] == 'DC') |\
            (state_df['STATE'] == 'DE') | (state_df['STATE'] == 'NJ') |\
            (state_df['STATE'] == 'NY') | (state_df['STATE'] == 'CT') |\
            (state_df['STATE'] == 'RI') | (state_df['STATE'] == 'MA') |\
            (state_df['STATE'] == 'VT') | (state_df['STATE'] == 'NH') |\
            (state_df['STATE'] == 'ME')
        state_df.loc[northwest, 'REGION'] = 'Northwest'
        state_df.loc[southwest, 'REGION'] = 'Southwest'
        state_df.loc[southeast, 'REGION'] = 'Southeast'
        state_df.loc[northeast, 'REGION'] = 'Northeast'
        # Sorts the states descendingly based on values in 'DELAY_RATIO_TIME'.
        state_df = state_df.sort_values('MEAN_DELAY', ascending=False)
        plt.figure(figsize=(13.5, 7))
        sns.barplot(data=state_df, x='STATE', y='MEAN_DELAY', hue='REGION')
        plt.xticks(rotation=-55)
        plt.title('Average Arrival Delays by Arriving States')
        plt.xlabel('Arriving States')
        plt.ylabel('Delays (duration ratio)')
        plt.savefig('delay_per_states.png', bbox_inches='tight')

        return state_df

    def usa_map_delay(self, state_df, fig_size):
        """
        It takes the WA and STATE dataframe, and a integer: fig_zise and
        produces a U.S.A. map with different colors that represents the average
        delay-time-ratio, and fig_size determines how large the resulting
        graph is. The graph will be saved as 'flights_delay_mapping.png'.
        """
        # Filter and merge the dataframe for remaining only the necessary
        # columns, and remaining only the unrepeated rows.
        rep_map_df = self._wa_df.loc[:, ['STATE', 'geometry']]
        print(type(rep_map_df))
        print(type(state_df))
        rep_map_df = rep_map_df.merge(state_df, left_on='STATE',
                                      right_on='STATE', how='right')
        map_df = rep_map_df.drop_duplicates()
        # Scaling the map and arranging the length of the legend to make the
        # graph visibly-friendly.
        map_gdf = gpd.GeoDataFrame(map_df, geometry='geometry')
        map_gdf.plot(column='MEAN_DELAY', legend=True,
                     figsize=(fig_size, fig_size))
        plt.savefig('flights_delay_mapping.png')

    # Flight delays distribution across all months
    def month_delay(self, seri_standard):
        """
        It takes a dataframe and produces a 3×4 matrix of histogram, each one
        shows the distribution of flight delays in each months. If there's no
        flight records in some months based on some inputing dataframe, the
        corresponding histogram should be left as blank white. The graph will
        be saved as 'delay_per_months.png'.
        """
        # Creates a plot axis to arrange each subplot in a 3×4 matrix.
        fig, [[ax1, ax2, ax3, ax4], [ax5, ax6, ax7, ax8],
              [ax9, ax10, ax11, ax12]]\
            = plt.subplots(3, 4, figsize=(40, 18), sharey=True)
        ax_lst = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11,
                  ax12]
        month_lst = ['January', 'Feburary', 'March', 'April', 'May', 'June',
                     'July', 'August', 'September', 'October', 'November',
                     'December']
        # Plot each month's flight delay distribution by looping 12 times.
        wa_df = self._wa_df
        for i in range(12):
            sns.histplot(data=wa_df[(wa_df['MONTH'] == i+1) &
                                    (wa_df['ARRIVAL_DELAY'] >= seri_standard) &
                                    (wa_df['ARRIVAL_DELAY'] <= 220)],
                         x='ARRIVAL_DELAY', ax=ax_lst[i], bins=35)
            ax_lst[i].set_xlabel('Delays (min)')
            ax_lst[i].set_ylabel('Number of Flights')
            ax_lst[i].set_title(month_lst[i])
        plt.title('Average Arrival Delays by Months')
        plt.savefig('delay_per_months.png')

    # Flight delays distribution across all days in a week
    def week_days_delay(self, seri_standard):
        """
        It takes the WA dataframe and produces a 3×3 matrix of histogram, 7 of
        the 9 plots show the distribution of flight delays in each days in a
        week. If there's no flight records in some days, the corresponding
        histogram should be left as blank white. The graph will be saved as
        'delay_per_week_days.png'.
        """
        # Creates a plot axis to arrange each subplot in a 3×3 matrix.
        fig, [[ax1, ax2, ax3], [ax4, ax5, ax6], [ax7, ax8, ax9]]\
            = plt.subplots(3, 3, figsize=(30, 18), sharey=True)
        ax_lst = [ax1, ax2, ax3, ax4, ax5, ax6, ax7]
        week_lst = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
        # Plot each days in a week's flight delay distribution by looping 7
        # times.
        wa_df = self._wa_df
        for i in range(7):
            sns.histplot(data=wa_df[(wa_df['DAY_OF_WEEK'] == i+1) &
                                    (wa_df['ARRIVAL_DELAY'] >= seri_standard) &
                                    (wa_df['ARRIVAL_DELAY'] <= 220)],
                         x='ARRIVAL_DELAY', ax=ax_lst[i], bins=35)
            ax_lst[i].set_xlabel('Delays (min)')
            ax_lst[i].set_ylabel('Number of Flights')
            ax_lst[i].set_title(week_lst[i])
        plt.title('Average Arrival Delays by Days in a Week')
        plt.savefig('delay_per_week_days.png')

    def departure_delay_correlation(self):
        """
        It takes the WA dataframe and produces a scatter plot which shows the
        correlation between departure delay and arrival delay. The graph will
        be saved as 'departure_to_arrival.png'.
        """
        sns.relplot(x='DEPARTURE_DELAY', y='ARRIVAL_DELAY', data=self._wa_df)
        plt.title('Correlation between Departure Delay and Arrival Delay')
        plt.xlabel('Departure Delay')
        plt.ylabel('Arrival Delay')
        plt.savefig('departure_to_arrival.png', bbox_inches='tight')

    def taxi_out_delay_correlation(self):
        """
        It takes the WA dataframe and produces a scatter plot which shows the
        correlation between "taxi out duration" and arrival delay. The graph
        will be saved as 'taxi_out_to_arrival.png'.
        """
        sns.relplot(x='TAXI_OUT', y='ARRIVAL_DELAY', data=self._wa_df)
        plt.title('Correlation between TAXI-OUT Duration and Arrival Delay')
        plt.xlabel('Duration of Plane Sliding in the Origin Airport')
        plt.ylabel('Arrival Delay')
        plt.savefig('taxi_out_to_arrival.png', bbox_inches='tight')

    def taxi_in_delay_correlation(self):
        """
        It takes the WA dataframe and produces a scatter plot which shows the
        correlation between "taxi in duration" and arrival delay. The graph
        will be saved as 'taxi_in_to_arrival.png'.
        """
        sns.relplot(x='TAXI_IN', y='ARRIVAL_DELAY', data=self._wa_df)
        plt.title('Correlation between TAXI-IN Duration and Arrival Delay')
        plt.xlabel('Duration of Plane Sliding in the Destination Airport')
        plt.ylabel('Arrival Delay')
        plt.savefig('taxi_in_to_arrival.png', bbox_inches='tight')
