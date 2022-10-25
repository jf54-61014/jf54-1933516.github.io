"""
This module contains a data_manipulation class used to manipulate datas.
"""


class data_manipulation:
    """
    This class contains functions to clean, merge and add the desired data
        for the visualization and machine learning function.
    """
    def __init__(self, airlines, airports, flights, states):
        """
        It takes the four dataframe as parameter,
        and initialize the status of the four dataframe for
        the following functions
        """
        self._airlines = airlines
        self._airports = airports
        self._flights = flights
        self._states = states

    def data_ML(self):
        """
        This function merges the airlines, airports, and flights dataframe,
        and clean the data to the form that suitable for
        machine learning models
        """
        flights = self._flights.rename(columns={'AIRLINE': 'ABBR_AIRLINE'})
        new_df = flights.merge(self._airlines, left_on='ABBR_AIRLINE',
                               right_on='IATA_CODE', how='left')
        new_df = new_df.merge(self._airports, left_on='DESTINATION_AIRPORT',
                              right_on='IATA_CODE', how='left')
        new_df = new_df.loc[:, ['MONTH', 'ABBR_AIRLINE', 'ORIGIN_AIRPORT',
                                'DEPARTURE_DELAY', 'TAXI_OUT',
                                'SCHEDULED_TIME', 'DISTANCE',
                                'ARRIVAL_DELAY',
                                # 'TAXI_IN', 'ELAPSED_TIME',
                                'DESTINATION_AIRPORT', 'AIRPORT', 'STATE',
                                'AIRLINE']]
        new_df = new_df[(new_df['ORIGIN_AIRPORT'] == 'BLI') |
                        (new_df['ORIGIN_AIRPORT'] == 'GEG') |
                        (new_df['ORIGIN_AIRPORT'] == 'PSC') |
                        (new_df['ORIGIN_AIRPORT'] == 'SEA')]
        # the destination airport data in month 10 is wrong. We choose to avoid
        # considering data in October also because there're no data about
        # October for WA as departure state. Also, in the scope of the nation,
        # we observe that October as a feature presents a very similar impact
        # in the delay time as the other common months. Thus, it is safe and
        # efficient to avoid month = 10 in the machine learning.
        new_df = new_df[new_df['MONTH'] != 10]
        Delay_ratio_time = new_df['DEPARTURE_DELAY'] / new_df['SCHEDULED_TIME']
        Delay_ratio_distance = new_df['DEPARTURE_DELAY'] / new_df['DISTANCE']
        new_df['DELAY_RATIO_TIME'] = Delay_ratio_time
        new_df['DELAY_RATIO_DISTANCE'] = Delay_ratio_distance

        return new_df

    def data_visual_all(self):
        """
        It takes four dataframe, merges the four dataframes into one final
        version based on shared columns, adds some new columns based on the
        existed columns, and returns the revised dataframe.
        """
        flights = self._flights.rename(columns={'AIRLINE': 'ABBR_AIRLINE'})
        # Rename the values in 'STATE' column so the "states" dataframe's
        # 'STATE' column can be matched with other dataframes.
        abbre_state = {
            "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
            "California": "CA", "Colorado": "CO", "Connecticut": "CT",
            "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
            "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
            "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME",
            "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
            "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
            "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
            "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
            "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
            "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
            "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
            "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
            "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
            "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI",
            "Wyoming": "WY", "District of Columbia": "DC",
            "American Samoa": "AS", "Guam": "GU",
            "Northern Mariana Islands": "MP", "Puerto Rico": "PR",
            "United States Virgin Islands": "VI"
        }
        self._states['NAME'] = self._states['NAME'].map(abbre_state).\
            fillna(self._states['NAME'])
        # Merge the dataframes, drop irrelevant columns and add new calculated
        # columns.
        new_df = flights.merge(self._airlines, left_on='ABBR_AIRLINE',
                               right_on='IATA_CODE', how='left')
        new_df = new_df.merge(self._airports, left_on='DESTINATION_AIRPORT',
                              right_on='IATA_CODE', how='left')
        new_df = new_df.loc[:, ['MONTH', 'ABBR_AIRLINE', 'ORIGIN_AIRPORT',
                                'DESTINATION_AIRPORT', 'DEPARTURE_DELAY',
                                'TAXI_OUT', 'SCHEDULED_TIME', 'ELAPSED_TIME',
                                'DISTANCE', 'TAXI_IN', 'ARRIVAL_DELAY',
                                'AIRPORT', 'STATE', 'LATITUDE', 'LONGITUDE',
                                'AIRLINE', 'DAY_OF_WEEK']]
        Delay_ratio_time = new_df['ARRIVAL_DELAY'] / new_df['SCHEDULED_TIME']
        Delay_ratio_distance = new_df['ARRIVAL_DELAY'] / new_df['DISTANCE']
        new_df['DELAY_RATIO_TIME'] = Delay_ratio_time
        new_df['DELAY_RATIO_DISTANCE'] = Delay_ratio_distance
        new_df = new_df.merge(self._states, left_on='STATE', right_on='NAME',
                              how='left')

        return new_df

    # Create, merge and revise dataframes (Only Departure from Washington
    # states).
    def data_visual_wa(self, new_df):
        """
        It takes the revised dataframe, filters the rows that only contains the
        flights that depart from Washington State, and returns the WA
        dataframe.
        """
        wa_df = new_df[(new_df['ORIGIN_AIRPORT'] == 'BLI') |
                       (new_df['ORIGIN_AIRPORT'] == 'GEG') |
                       (new_df['ORIGIN_AIRPORT'] == 'PSC') |
                       (new_df['ORIGIN_AIRPORT'] == 'SEA')]
        return wa_df

    def seriously_delay(self, wa_df):
        """
        It takes the WA dataframe and returns a tuple, which the first value
        is a dataframe added a new categorical column, which represents
        whether the flight is seriously delayed or not, and the second value
        is a numerical value which seperates the "seriously delayed" from
        "unseriously delayed"
        """
        standard1 = wa_df['DELAY_RATIO_TIME'].quantile(0.75)
        standard2 = wa_df['DELAY_RATIO_TIME'].mean() +\
            wa_df['DELAY_RATIO_TIME'].std()
        seri_standard = 0.5*standard1 + 0.5*standard2
        # Adds the new column: 'seriously_dely' to the dataframe wa_df.
        wa_df['seriously_delay'] = wa_df['DELAY_RATIO_TIME']\
            .apply(lambda x: 0 if x < seri_standard else 1)
        return (wa_df, seri_standard)
