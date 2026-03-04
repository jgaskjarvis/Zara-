from time import sleep
from jnius import autoclass

# Background mein service ko active rakhne ke liye
while True:
    print("ZARA Background Service is listening...")
    sleep(15)
