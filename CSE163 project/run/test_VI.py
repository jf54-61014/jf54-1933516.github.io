"""
This program contains several test functions to test each function's performing
capacity in both plot.py and machine_learning.py modules.
"""
from plot import plot


class visual_test:
    """
    This class aims to test the visualization programs we did in the main
        modules
    """
    def __init__(self, wa_df, num):
        """
        Initializing this class
        Merge and create a test dataframe with only 3 rows.
        """
        self._wa_df = wa_df
        self._test_df = wa_df.sample(n=num)
        print(self._test_df)
        self._plotting = plot(self._test_df)

    def test_total_flights(self):
        """
        This testing function is to test the total_flights plot
        """
        self._plotting.total_flights()

    def test_delay_ratio_time_distance(self):
        """
        This function is to test the delay_ratio_time distance plot
        """
        self._plotting.delay_ratio_time_distance()

    def test_airlines_delay(self):
        """
        This function is to test the airlines_delay plot
        """
        self._plotting.airlines_delay()

    def test_states_delay(self):
        """
        This function is to test the states_delay plot
        """
        self._plotting.states_delay()

    def test_usa_map_delay(self, state_df, fig_size):
        """
        This function is to test the usa_map_delay plot. It takes the state_df
        and fig_size as parameters, and returns the usa_map_delay plot.
        """
        self._plotting.usa_map_delay(state_df, fig_size)

    def test_month_delay(self, seri_standard):
        """
        This function is to test the month_delay plot. It takes seri_standard
        as the parameter and will return the plot of month_delay.
        """
        self._plotting.month_delay(seri_standard)

    def test_week_days_delay(self, seri_standard):
        """
        This function is to test the week_days_delay plot. It takes the
        seri_standard as the parameter and will return the plot
        ofweek_days_delay
        """
        self._plotting.week_days_delay(seri_standard)

    def test_departure_delay_correlation(self):
        """
        This function is to test the departure_delay_correlation plot.
        """
        self._plotting.departure_delay_correlation()

    def test_taxi_out_delay_correlation(self):
        """
        This function is to test the axi_out_delay_correlation plot.
        """
        self._plotting.taxi_out_delay_correlation()

    def test_taxi_in_delay_correlation(self):
        """
        This function is to test the taxi_in_delay_correlation plot.
        """
        self._plotting.taxi_in_delay_correlation()
