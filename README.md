# bionic_arm
Files used for controlling a bionic arm. The arm consists of three fingers controlled by Actuonix PQ-12-P linear motors, and Dynamixel MX-28 motor for controlling the wrist. Odroid XU-4 with Ubuntu 15.04 installed is used. Motors are controlled by GPIO pins 13,15,17,18,19,20 for linear motors and UART for serial communication with MX-28, and an additional Control board is used because GPIO outputs are 1.8 V, but all motors need 12 V. 

Follow the TUTORIAL in order to prepare Odroid XU-4 for using the program.

"control.py" file needs to be copied to the Odroid XU-4 and script.sh file which initializes all the GPIO outputs for use needs to be created using: 
```
sudo nano script.sh 
```
(vi can be used instead of nano)

To run the program just type the following line in Terminal: 
```
sudo ./script.sh
```
