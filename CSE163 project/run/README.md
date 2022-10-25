# GUIDE TO RUN THE PROJECT

## Before you try to manipulate this entire project by yourself, let's first see what are contained in this compressed zip file.

### 1. 6 python module files

    plot.py: usable codes for drawing visualization plots to see flight delay patterns.

    ML_Model.py: usable codes for training models to predict flights delay behavior.

    Data_manipulation.py: codes to merge data frames to different versions assists to other python files.

    main.py: calls function in other four modules to run the python codes in total.

    test_VI.py: functioning codes for test all functions in plot.py

    test_ML.py: functioning codes for test all functinos in ML_Model.py

### 2. 1 MarkDown file

    README.md: contains the instruction to manipulate and run this entire project.

### 3. 7 files started with "cb_2018_"

    These files worked together to create the shape file available for Geopandas to read in as a GeoDataFrame.

### 4. 1 PDF file

    FinalReport-CSE163-AJY.pdf: the final version of Report of this project, you can read it for more business intellegence hint about taking flights in you are interested in.

## Step 0: Dowanloading the 3 datasets "flights.csv, airlines.csv, airports.csv" from this link: https://www.kaggle.com/datasets/usdot/flight-delays, and put the 3 datasets to the same folder as zipped.

## Step 1: Put all of the files above into one single folder if they are not.

## Step 2: Open the folder in Step 1 with Visual Studio Code.

## Step 3: Run visualization part:

    1. comment out all the functions from line 41 to line 55.

    2. Go to main.py line 49, "plotting.usa_map_delay(state_df, fig_size)". Then, set the "fig_size" parameter to "fig_size = 72".

    3. Click "Run" bottum to run the main.py file (this running process may takes about 4~5 minutes) 

    4. Check whether several new .png graph files have been saved to the same folder. If so, change the name of the "flights_delay_mapping.png" into "flights_delay_mapping_72.png"

    5. Repeat the process of 2 but change "fig_size = 72" to "fig_size = 11".

    6. Click "Run" bottum to run the main.py file (this running process may takes about 4~5 minutes) 

    7. Now combine the map in "flights_delay_mapping_72.png" and legend column in "flights_delay_mapping.png" by photo editing to make the size readable, now you get the similar map graph as appeared in the Report.

## Step 4: Run Machine Learning part:

    1. Uncomment all functions from the previous step.

    2.Run code in main.py from line 57 to 68, some of the models may take a
      while to run, so be patient!

    3. Now you will see all the results be printed and all the graphs stored

## Step 5: Run Test of Visualization Part:

    1. Uncomment all functions from the previous step.

    2. comment out all the functions (from line 28 to line 39) and (from line 56 to line 75).

    3. Click "Run" bottum to run the main.py file (this running process may takes about 1.5 minutes).

    4. Now you can view the printed "test dataframe"'s result in the terminal through the function of printing the vi_test in the test_VI module.

    5. You can determine whether each symbol in each plot is in the correct position by calculating the value in each point by information in the printed dataframe in the terminal.

## Step 6: Run Test of Machine Learning Part:

    1. Uncomment all functions from the previous step.

    2. comment out all the functions (from line 28 to line 55) and (from line 70 to line 75).

    3. Click "Run" bottum to run the main.py files

    4. Now you can see the result of all the tests and the
       visualizations. 

### That's all you should do to experience how to get the same results as appeared on the Report! Congratulations! It's a nice day and you can use the day to do something else, but now, YOU MADE IT!