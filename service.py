from time import sleep
from jnius import autoclass
from android import AndroidService

# Background mein service ko zinda rakhne ke liye logic
def run_service():
    while True:
        # Ye line logs mein dikhayegi ki ZARA active hai
        print("ZARA Background Service: Listening for commands...")
        
        # 15 second ka sleep battery bachane ke liye zaroori hai
        sleep(15)

if __name__ == '__main__':
    run_service()
