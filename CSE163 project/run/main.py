import pandas as pd
import geopandas as gpd
from test_ML import test_ml
# the flake8 problem is because we commend our machine learning function
# from ML_Model import ML_Model
from Data_manipulation import data_manipulation
# from plot import plot
# from test_VI import visual_test

"""
This module runs our projects for both visualization and machine learning
    model part
"""


def main():
    airlines = pd.read_csv('run/airlines.csv')
    airports = pd.read_csv('run/airports.csv')
    flights = pd.read_csv('run/flights.csv', low_memory=False)
    states = gpd.read_file('run/cb_2018_us_state_500k.shp')

    data = data_manipulation(airlines, airports, flights, states)

    # data_vi = data.data_visual_all()
    # wa_df = data.data_visual_wa(data_vi)
    # wa_df, seri_standard = data.seriously_delay(wa_df)

    # plotting = plot(wa_df)
    # plotting.total_flights()
    # plotting.delay_ratio_time_distance()
    # plotting.airlines_delay()
    # plotting.states_delay()
    # state_df = plotting.states_delay()
    # plotting.usa_map_delay(state_df, 72)
    # plotting.month_delay(seri_standard)
    # plotting.week_days_delay(seri_standard)
    # plotting.departure_delay_correlation()
    # plotting.taxi_out_delay_correlation()
    # plotting.taxi_in_delay_correlation()

    # uncomment the followings to run the test for the visualization
    # plotting = plot(wa_df)
    # state_df = plotting.states_delay()
    # vi_test = visual_test(wa_df, 3)
    # vi_test.test_total_flights()
    # vi_test.test_delay_ratio_time_distance()
    # vi_test.test_airlines_delay()
    # vi_test.test_states_delay()
    # vi_test.test_usa_map_delay(state_df, 72)
    # vi_test.test_month_delay(seri_standard)
    # vi_test.test_week_days_delay(seri_standard)
    # vi_test.test_departure_delay_correlation()
    # vi_test.test_taxi_out_delay_correlation()
    # vi_test.test_taxi_in_delay_correlation()
# =================================================================

    data_ml = data.data_ML()
    data_ml = data.seriously_delay(data_ml)[0]

    # print('Model with all the data:')
    # flights_all = ML_Model(data_ml, 'all')
    # flights_all.dt_classification()
    # flights_all.plot_dt_classification()
    # flights_all.dt_regression()
    # flights_all.plot_dt_regression()
    # flights_all.linear_regression()
    # flights_all.knn_classification()
    # flights_all.knn_regression()

    # uncommend followings to run the test for Machine Learning Model
    ml_test = test_ml(data_ml)
    # ml_test.test_models(100)
    # ml_test.test_models(1000)
    ml_test.test_models(10000)

    print('DONE!!')


if __name__ == '__main__':
    main()
