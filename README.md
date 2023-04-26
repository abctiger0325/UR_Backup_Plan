## Package Required to install

- Trimesh

- Numpy

- Matplotlib

- Pygrabber

- CV2

## How to use

1. Call base.py in console

    - Console will display avaible camera, select camera by input the camera index

2. Press 'Q' to capture the camera image contain the reference object and coral head

    - Rememeber foucs the image window before process

3. Captured image will be displayed in new window

    - Draw the line by click the start point and end point of the line

    - Please draw the line in the following sequence:

        1. Reference Object's width

        2. Base Radius Length

        3. Height of Coral

        4. Top Radius Length

    - Drawn line will be displayed on screen with the length calculated

    - Lenght will also print in console

    - Press 'Q' to process to next step

4. Input the calculated value according to the console required

    - The coordinate of 3 area is using latitude and longitude

        - Latitude is deviding the coral head into 4 levels, 1 at the lowest and 4 at the highest

        - Longitude is using clock direction, can assume the first object at 12 o'clock direction first

    - The model will be displayed in matplotlib window, right click to Zoom out and left click to rotate

    - Dimensions and Areas of dieased area is also displayed