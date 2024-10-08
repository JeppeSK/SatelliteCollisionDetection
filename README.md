# Satellite Collision Detection

### `About`

This is a simple program, with the intent of using Machine Learning to predict possible collisions between satellites.

### `How does it work?`

When running the program, you'll notice a processing bar in the terminal, this bar shows the rate which the satellites are being processed, and gives an estimate on how long the task would take:

![Processing Satellites](https://github.com/user-attachments/assets/a84e0979-ec43-46a3-b448-9709ed0957bc)

When finished processing, plotly ensure to provide a 3d Graph, with the Earth plottet as a blue sphere, and the satellites as green dots. The line between the satellites show the possible collisions.
Here is a image as reference:

![Plotly image](https://github.com/user-attachments/assets/ac0afed4-6ced-48b2-bacc-23d893f59dad)

### `Changing the dataset`

If you wish to change the dataset and use you're own data to teach the ML and predict your own collisions follow these steps.

1. Delete the file satellite_collision_model.joblib - This file provides the ML with the data it's already been taught
2. Delete the file satellites.csv - This file holds the different satellites already processed and converted to a csv file.
3. Navigate to Convert_data_to_csv.py
4. In the script "Convert_data_to_csv.py" at line 10, a url is provided from which the data is recieved. Change this url to your disired API/own datasheet

It is important to note, that changing the csv_file name to something else, will require further changes to the main.
Also this project is strictly for learning the use of Machine Learning in different scenarios. And certain flaws/bugs is to be expected.
