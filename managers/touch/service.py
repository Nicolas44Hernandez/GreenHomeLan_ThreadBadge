from interfaces.touch import Touch_CST816T
from interfaces.lcd import LCD_1inch28
import time

class TouchManager:
    """Manager for Touch interface"""

    touch: Touch_CST816T
    # If True allow touch in screen, if false swipe allowed
    touch_allowed: bool
    
    def setup(self, LCD: LCD_1inch28, mode: int=1 ):
        """Setup touch interface"""
        # Create Touch interface
        self.touch=Touch_CST816T(mode=mode,LCD=LCD)

        # Set init status
        self.touch_allowed =True
    
    
    def setMode(self, mode: int):
        """Set touch mode"""
        self.touch.Mode = mode
        self.touch.Set_Mode(self.touch.Mode)


    def waitForTouch(self):
        """Wait for button press"""

        print("waitForTouch...") 

        x = y = data = 0
        self.touch.Flgh = 0
        self.touch.Flag = 0
        self.touch.Mode = 1
        self.touch.Set_Mode(self.touch.Mode)
        
        #self.touch.tim.init(period=1, callback=self.touch.Timer_callback)
        while True:
            if self.touch.Flgh == 0 and self.touch.X_point:
                self.touch.Flgh = 1
                x = self.touch.X_point
                y = self.touch.Y_point

            if self.touch.Flag == 1:
                time.sleep(0.25)
                self.touch.Flag = 0
                self.touch.l=0                        
                x = self.touch.X_point
                y = self.touch.Y_point
                if x < 120 and y < 120:
                    return 1
                if x > 120 and y < 120:
                    return 2
                if x < 120 and y > 120:
                    return 3
                if x > 120 and y > 120:
                    return 4
    
    def waitForSwipe(self):
        self.touch.Mode = 0
        self.touch.Set_Mode(self.touch.Mode)

        gesture = 0 
        while gesture != 3 and gesture != 4:
            gesture = self.touch.Gestures
            time.sleep(0.1)

        if gesture == 3:
            self.touch.Mode = 1
            self.touch.Set_Mode(self.touch.Mode)
            self.touch.Gestures = "None"
            return False
            
        if gesture == 4:
            self.touch.Mode = 1
            self.touch.Set_Mode(self.touch.Mode)
            self.touch.Gestures = "None"
            return True


touch_manager_service: TouchManager = TouchManager()
""" Touch manager service singleton"""
