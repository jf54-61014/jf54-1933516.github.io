"""
This module contains a ML_Model class for all the machine learning function
"""
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
# from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor,\
    plot_tree
from sklearn.preprocessing import StandardScaler  # scaling for data!
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neighbors import KNeighborsRegressor


class ML_Model:
    """
    A ML_Model represents a bunch of machine learning models for the given
    dataset.
    """

    def __init__(self, df, size):
        """
        Implement an initializer for the class ML_Model.
        It takes in a data set and a string describing the size of the dataset.
        """
        self._df = df
        self._size = size

    def dt_regression(self):
        '''
        It trains a decision tree regression model to predict the arrival
        delay time of a flight given its flight status information. It prints
        a dataframe showing the MSE, RMSE and MAE under the different maximun
        tree depth. And plots the relationship between the errors and maximun
        decision tree depth.
        '''
        data = self._df.loc[:, ['ARRIVAL_DELAY', 'MONTH', 'ABBR_AIRLINE',
                                'ORIGIN_AIRPORT', 'DEPARTURE_DELAY',
                                'TAXI_OUT', 'SCHEDULED_TIME',
                                # 'ELAPSED_TIME', 'TAXI_IN',
                                'DISTANCE',
                                'DESTINATION_AIRPORT']].dropna()
        X = data.loc[:, data.columns != 'ARRIVAL_DELAY']
        X = pd.get_dummies(X)
        y = data['ARRIVAL_DELAY']
        X_train, X_test, y_train, y_test =\
            train_test_split(X, y, test_size=0.2, random_state=10)

        y_mse = []
        y_rmse = []
        y_mae = []
        accuracies = []
        for i in range(1, 30):
            model = DecisionTreeRegressor(max_depth=i)
            model.fit(X_train, y_train)

            X_predictions = model.predict(X_train)
            y_predictions = model.predict(X_test)
            X_mse_value = mean_squared_error(y_train, X_predictions)
            y_mse_value = mean_squared_error(y_test, y_predictions)
            X_rmse_value = mean_squared_error(y_train, X_predictions,
                                              squared=False)
            y_rmse_value = mean_squared_error(y_test, y_predictions,
                                              squared=False)
            X_mae_value = mean_absolute_error(y_train, X_predictions)
            y_mae_value = mean_absolute_error(y_test, y_predictions)

            y_mse.append(y_mse_value)
            y_rmse.append(y_rmse_value)
            y_mae.append(y_mae_value)
            accuracies.append({'max depth': i, 'train mse': X_mse_value,
                               'test mse': y_mse_value,
                               'train rmse': X_rmse_value,
                               'test rmse': y_rmse_value,
                               'train mae': X_mae_value,
                               'test mae': y_mae_value})
        # train rmse': X_rmse, 'test rmse': y_rmse
        print("Decision Tree Regression: tree depth vs errors:")
        print(pd.DataFrame(accuracies))

        tree_depth = list(range(1, 30))
        fig2 = plt.figure()
        plt.plot(tree_depth, y_mse, label="y MSE")
        plt.plot(tree_depth, y_rmse, label="y RMSE")
        plt.plot(tree_depth, y_mae, label="y MAE")
        plt.title(f'different errors with tree depth with n={self._size}')
        plt.xlabel('tree depth')
        plt.ylabel('error')
        plt.legend()
        fig2.savefig(f'different_errors_with_tree_depth_n={self._size}.png')

    def plot_dt_regression(self):
        '''
        This function plot the decision tree for regression model.
        '''
        data = self._df.loc[:, ['ARRIVAL_DELAY', 'MONTH', 'ABBR_AIRLINE',
                                'ORIGIN_AIRPORT', 'DEPARTURE_DELAY',
                                'TAXI_OUT', 'SCHEDULED_TIME',
                                # 'ELAPSED_TIME', 'TAXI_IN',
                                'DISTANCE',
                                'DESTINATION_AIRPORT']].dropna()
        X = data.loc[:, data.columns != 'ARRIVAL_DELAY']
        X = pd.get_dummies(X)
        y = data['ARRIVAL_DELAY']
        X_train, X_test, y_train, y_test =\
            train_test_split(X, y, test_size=0.2, random_state=10)

        model = DecisionTreeRegressor(max_depth=3)
        model.fit(X_train, y_train)
        fig1 = plt.figure()
        plot_tree(model, feature_names=list(data.columns[1:]),
                  class_names=list(data.columns[0]), filled=True)
        fig1.savefig(f'Decision_Tree_Regression_n={self._size}.png')

    def dt_classification(self):
        '''
        The function trains a decision tree classification model to predict
        the arrival delay.
            time of a flight given its flight status information
        It returns the accuracy representing the accuracy of the prediction
        with different decision tree depth. And it plots the relationship
        between the prediction accuracy and maximun decision tree depth.
        '''
        data = self._df.loc[:, ['seriously_delay', 'MONTH', 'ABBR_AIRLINE',
                                'ORIGIN_AIRPORT', 'DEPARTURE_DELAY',
                                'TAXI_OUT', 'SCHEDULED_TIME',
                                # 'ELAPSED_TIME', 'TAXI_IN',
                                'DISTANCE', 'DESTINATION_AIRPORT',
                                'AIRLINE']].dropna()
        X = data.loc[:, data.columns != 'seriously_delay']
        X = pd.get_dummies(X)
        y = data['seriously_delay']
        X_train, X_test, y_train, y_test =\
            train_test_split(X, y, test_size=0.2, random_state=10)

        X_accuracy = []
        y_accuracy = []
        accuracies = []
        for i in range(1, 20):
            model = DecisionTreeClassifier(criterion="entropy", max_depth=i)
            model.fit(X_train, y_train)

            X_acc = model.score(X_train, y_train)
            y_acc = model.score(X_test, y_test)

            X_accuracy.append(X_acc)
            y_accuracy.append(y_acc)
            accuracies.append({'max depth': i, 'train accuracy': X_acc,
                               'test accuracy': y_acc})
        print("Decision Tree Classification: tree depth vs accuracy:")
        print(pd.DataFrame(accuracies))
        # print(f"max depth: {i}, train accuracy: {X_acc}, test accuracy:
        # {y_acc}")

        # We choose max_depth=14 since the accuracy is the highest with the
        # decision tree of max depth 14
        print()
        print('Decision Tree Classification: matrix and report with depth 3:')
        model = DecisionTreeClassifier(criterion="entropy", max_depth=3,
                                       random_state=10)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))

        tree_depth = list(range(1, 20))
        fig2 = plt.figure()
        plt.plot(tree_depth, X_accuracy, label="train accuracy")
        plt.plot(tree_depth, y_accuracy, label="test accuracy")
        plt.title(f'Train vs test accuracy by tree depth with n={self._size}')
        plt.xlabel('tree depth')
        plt.ylabel('accuracy')
        plt.legend()
        fig2.savefig(f'Train_vs_test_accuracy_by_tree_depth_n=\
            {self._size}.png')

    def plot_dt_classification(self):
        """
        This function plots the decision tree for classification model
        """
        data = self._df.loc[:, ['seriously_delay', 'MONTH', 'ABBR_AIRLINE',
                                'ORIGIN_AIRPORT', 'DEPARTURE_DELAY',
                                'TAXI_OUT', 'SCHEDULED_TIME',
                                # 'ELAPSED_TIME', # 'TAXI_IN',
                                'DISTANCE',  'DESTINATION_AIRPORT',
                                'AIRLINE']].dropna()
        X = data.loc[:, data.columns != 'seriously_delay']
        X = pd.get_dummies(X)
        y = data['SERIOUSLY_DELAY']
        X_train, X_test, y_train, y_test =\
            train_test_split(X, y, test_size=0.2, random_state=10)

        model = DecisionTreeClassifier(criterion="entropy", max_depth=3)
        model.fit(X_train, y_train)
        fig1 = plt.figure(figsize=(50, 40))
        plot_tree(model, feature_names=list(data.columns[1:]),
                  class_names=list(data.columns[0]), filled=True)
        fig1.savefig(f'Decision_Tree_Classification_n={self._size}.png')

    def linear_regression(self):
        '''
        It trains a linear regression model to predict the arrival delay time
        of a flight given its flight status information. It prints out a
        summary for the linear regression model about how well it performs on
        prediction.
        '''
        data = self._df[['MONTH', 'ABBR_AIRLINE', 'DEPARTURE_DELAY',
                         'ORIGIN_AIRPORT', 'TAXI_OUT', 'SCHEDULED_TIME',
                         'DISTANCE',
                         # 'TAXI_IN', 'ELAPSED_TIME',
                         'DESTINATION_AIRPORT', 'AIRLINE',
                         'ARRIVAL_DELAY']].dropna()
        X = data.loc[:, data.columns != 'ARRIVAL_DELAY']
        X = pd.get_dummies(X)
        X['intercept'] = 1
        y = data[['ARRIVAL_DELAY']]

        X_train, X_test, y_train, y_test =\
            train_test_split(X, y, test_size=0.2, random_state=30)
        ols = sm.OLS(y_train, X_train)
        ols_result = ols.fit()
        print("Linear Regression summary:")
        print(ols_result.summary())
        print()

    def knn_classification(self):
        '''
        This function creates a k-nearest neighbors (KNN) algorithm
        Classification to predict whetehr a flight would be 'Seriously
        Delayed'. The results of the KNN classification, evaluations, and
        related plots will be produced.
        '''
        data = self._df[['MONTH', 'ABBR_AIRLINE', 'DEPARTURE_DELAY',
                         'ORIGIN_AIRPORT', 'TAXI_OUT', 'SCHEDULED_TIME',
                         'DISTANCE',
                         # 'TAXI_IN', 'ELAPSED_TIME',
                         'DESTINATION_AIRPORT', 'AIRLINE',
                         'seriously_delay']].dropna()
        X = data.loc[:, data.columns != 'seriously_delay']
        X = pd.get_dummies(X)
        y = data[['seriously_delay']]

        X_train, X_test, y_train, y_test =\
            train_test_split(X, y, test_size=0.2, random_state=10)

        # fitting data into scaler to make later processing fair and reasonable
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        # set and fit the KNN classification model
        classifier = KNeighborsClassifier(n_neighbors=3)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        print("KNN Classification: matrix and report")
        # this is the confusion matrix producing a matrix generalizing and
        # describing the performance of the KNN classification model
        print(confusion_matrix(y_test, y_pred))

        # Important! This table presents the model performances in specialize
        # and essential metrics precision, recall, f1-score, and accuracy
        # results
        print(classification_report(y_test, y_pred))

        X_accuracy = []
        y_accuracy = []
        accuracies = []
        for i in range(3, 14):
            model = KNeighborsClassifier(n_neighbors=i)
            model.fit(X_train, y_train)
            X_acc = model.score(X_train, y_train)
            y_acc = model.score(X_test, y_test)
            X_accuracy.append(X_acc)
            y_accuracy.append(y_acc)
            accuracies.append({'K Value': i, 'train accuracy': X_acc,
                               'test accuracy': y_acc})
        # the mean accuracy on the given test data and labels.
        print('KNN Classification accuracy vs K value')
        print(pd.DataFrame(accuracies))
        # print(i, accuracy[-1], accuracy[-1])

        plt.figure(figsize=(12, 6))
        plt.plot(range(3, 14), y_accuracy, label="test accuracy")
        plt.title(f'Accuracy vs K Value with n={self._size}')
        plt.xlabel('K Value')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.savefig(f'KNN_Clasification_Accuracy_K_Value_n={self._size}.png')

    def knn_regression(self):
        """
        This function creates a k-nearest neighbors (KNN) algorithm Regression
        to predict the flight delay time. The results of the KNN regression,
        evaluations, and related plots will be produced.
        """
        data = self._df[['MONTH', 'ABBR_AIRLINE', 'DEPARTURE_DELAY',
                         'ORIGIN_AIRPORT', 'TAXI_OUT', 'SCHEDULED_TIME',
                         'DISTANCE',
                         # 'TAXI_IN', 'ELAPSED_TIME',
                         'DESTINATION_AIRPORT', 'AIRLINE',
                         'ARRIVAL_DELAY']].dropna()
        X = data.loc[:, data.columns != 'ARRIVAL_DELAY']
        X = pd.get_dummies(X)
        y = data[['ARRIVAL_DELAY']]
        X_train, X_test, y_train, y_test =\
            train_test_split(X, y, test_size=0.2, random_state=10)

        # fitting data into scaler
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        Regressor = KNeighborsRegressor(n_neighbors=3)
        Regressor.fit(X_train, y_train)

        y_pred = Regressor.predict(X_test)  # predict the labels of test data
        mean_squared_error(y_pred, y_test)  # see the Mean Square Error

        # the part below is to find the best K number to do the KNN prediction
        y_mse = []
        y_rmse = []
        y_mae = []
        accuracies = []
        for K in range(3, 14):
            Regressor = KNeighborsRegressor(n_neighbors=K)
            Regressor.fit(X_train, y_train)  # fit the model
            y_pred = Regressor.predict(X_test)  # make prediction on test set
            # sm.tools.eval_measures.mse

            X_predictions = Regressor.predict(X_train)
            y_predictions = Regressor.predict(X_test)
            X_mse_value = mean_squared_error(y_train, X_predictions)
            y_mse_value = mean_squared_error(y_test, y_predictions)
            X_rmse_value = mean_squared_error(y_train, X_predictions,
                                              squared=False)
            y_rmse_value = mean_squared_error(y_test, y_predictions,
                                              squared=False)
            X_mae_value = mean_absolute_error(y_train, X_predictions)
            y_mae_value = mean_absolute_error(y_test, y_predictions)

            y_mse.append(y_mse_value)
            y_rmse.append(y_rmse_value)
            y_mae.append(y_mae_value)
            accuracies.append({'K value': K, 'train mse': X_mse_value,
                               'test mse': y_mse_value,
                               'train rmse': X_rmse_value,
                               'test rmse': y_rmse_value,
                               'train mae': X_mae_value,
                               'test mae': y_mae_value})

        print('KNN Regression MAE vs K value:')
        print(pd.DataFrame(accuracies))

        # visualizations
        plt.figure()
        # plt.plot(range(3, 14), accuracies)
        plt.plot(range(3, 14), y_mse, label="y MSE")
        plt.plot(range(3, 14), y_rmse, label="y RMSE")
        plt.plot(range(3, 14), y_mae, label="y MAE")
        plt.grid(True)
        plt.legend()
        plt.title(f'KNN Regression Performance with n={self._size}')
        plt.xlabel('K Value')
        plt.ylabel('errors')
        plt.savefig(f'KNN_Regression_K_value_vs_errors_n={self._size}.png')
