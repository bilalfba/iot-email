# -*- coding: utf-8 -*-
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import subprocess
import pygame
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
from getch import getch
import time                                #Import time library
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering n

TRIG = 20                                  #Associate pin 20 to TRIG
ECHO = 21                                  #Associate pin 21 to ECHO

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Raspberry Pi pin configuration:
lcd_rs        = 22  
lcd_en        = 27
lcd_d4        = 18
lcd_d5        = 17
lcd_d6        = 15
lcd_d7        = 14

GPIO.setmode(GPIO.BCM)


lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows)

def main():
       #run the program in a loop
       while(True):
                #check for someone to come near the robot
                lcd.message('The Assembly Bot')
                check_availability()
                #play the audio file to get the name
                pygame.mixer.init()
                pygame.mixer.music.load("hello.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy()==True:
                        continue
                #get the name
                name = get_data(1)
                print(name)
                #play the audio file to get email
                pygame.mixer.init()
                pygame.mixer.music.load("email.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy()==True:
                        continue
                #get the email
                email = get_data(0)
                print(email)
                lcd.message('Updating...')
                update(name, email)
                lcd.message('See you later!')
                #play the audio file 
                pygame.mixer.init()
                pygame.mixer.music.load("thankyou.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy()==True:
                        continue
              



def get_data(name):
        #clear the messages on lcd
        lcd.clear()
        print("getting data...")
        
        #check if the function is called to ask for name or email 
        if(name == 1):
                lcd.message('Enter your name: ')
        else:
             lcd.message('Enter your Email: ')
             
        #initialize a string to store the data from user 
        str = ''
        #wait for the user to enter a character 
        ch = getch()
        lcd.clear()

        #print the character to the lcd 
        lcd.message(ch)
        #add the chracter to the string
        str = str + ch
        #keep reading the data from user
        
        while True:
                ch = getch()
                print(ch)
                #convert to ascii
                ch1 = ord(ch)
                print(ch1)
                
                                
                #delete one character if user pressed backspace
                if(ch1 == 127): 
                        lcd.clear()
                        str = str[:-1]
                        lcd.message(str)
                        print(str)
                        print('backspace')
                        i = len(str)
                        while(i>16):
                                lcd.move_left()
                                i = i - 1
                                
                #exit the function and return the data if the user pressed enter 
                elif(ch1 == 10 or ch1 == 13):
                        lcd.clear()
                        return str

                else:
                     lcd.message(ch)
                     str = str + ch
                     #move the lcd's display to left if there are more than 16 characters
                     if(len(str) > 16):
                            lcd.move_left()


def check_availability():
        GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
        GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in

        while True:

              GPIO.output(TRIG, False)                 #Set TRIG as LOW
              print "Waitng For Sensor To Settle"
              time.sleep(2)                            #Delay of 2 seconds

              GPIO.output(TRIG, True)                  #Set TRIG as HIGH
              time.sleep(0.00001)                      #Delay of 0.00001 seconds
              GPIO.output(TRIG, False)                 #Set TRIG as LOW

              while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
                pulse_start = time.time()              #Saves the last known time of LOW pulse

              while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
                pulse_end = time.time()                #Saves the last known time of HIGH pulse 

              pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

              distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
              distance = round(distance, 2)            #Round to two decimal points

              if distance > 2 and distance < 50:      #Check whether the distance is within range
                return
              else:
                print "Out Of Range"                   #display out of range


def update(name, email):
    
    #Authorize your credentials
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
    gc = gspread.authorize(credentials)

    #Opening your worksheet
    wks = gc.open("Email List").sheet1


    #Initializing Test names
    rowToAdd = [name, email]

    # Appending the row to the end of the sheet
    wks.append_row(rowToAdd)

    print 'Done!'



if __name__ == "__main__":
    main()
