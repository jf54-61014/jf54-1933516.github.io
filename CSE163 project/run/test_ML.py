"""
This module contains a test_ml class to test the machine
learning function.
"""
from ML_Model import ML_Model


class test_ml:
    """
    This class is used to test the ML_Model that we wrote.
    """
    def __init__(self, df):
        """
        This function takes a dataframe and initialize the class to test
        machine learning
        """
        self._df = df

    def test_models(self, size):
        """
        This function takes a integer as parameter representing the size of
            the test data
        It runs and randomly for a subdataset with the given size
            and print out all the result for the test dataset.
        """
        print('---------------------------------------------------------')
        print('TESTING THE MODELS! ! ! ! ! ! ! ! ! ')
        print(f'Model with data size {size}:')
        test_data = ML_Model(self._df.sample(n=size), f'{size}')
        test_data.dt_classification()
        test_data.dt_regression()
        test_data.linear_regression()
        test_data.knn_classification()
        test_data.knn_regression()
