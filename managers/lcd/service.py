import math
from interfaces.lcd import LCD_1inch28


class LCDManager:
    """Manager for LCD interface"""

    lcd: LCD_1inch28
    current_wifi_status: bool
    current_presence_status: bool
    current_electricity_status: bool

    def setup(self, brightness: int=65535):
        # Create LCD interface
        self.lcd = LCD_1inch28()
        self.lcd.set_bl_pwm(brightness)

        # Set init status
        self.current_wifi_status=None
        self.current_presence_status=None
        self.current_electricity_status=None

        # Set init background
        self.showInitBackground()

    def drawRing(self, x,y,r,c):
        """Draw a ring"""
        self.lcd.pixel(x-r,y,c)
        self.lcd.pixel(x+r,y,c)
        self.lcd.pixel(x,y-r,c)
        self.lcd.pixel(x,y+r,c)        
        for i in range(1,r):
            a = int(math.sqrt(r*r-i*i)) # Pythagoras
            self.lcd.pixel(x-a,y-i,c)
            self.lcd.pixel(x+a,y-i,c)
            self.lcd.pixel(x-a,y+i,c)
            self.lcd.pixel(x+a,y+i,c)
            self.lcd.pixel(x-i,y-a,c)
            self.lcd.pixel(x+i,y-a,c)
            self.lcd.pixel(x-i,y+a,c)
            self.lcd.pixel(x+i,y+a,c)

    def drawCircle(self, x,y,r,c):
        """Draw a circle"""
        self.lcd.hline(x-r,y,r*2,c)
        for i in range(1,r):
            a = int(math.sqrt(r*r-i*i)) # Pythagoras!
            self.lcd.hline(x-a,y+i,a*2,c) # Lower half
            self.lcd.hline(x-a,y-i,a*2,c) # Upper half


    def DrawTriangle(self, x1,y1,x2,y2,x3,y3,c): # Draw outline triangle
        self.lcd.line(x1,y1,x2,y2,c)
        self.lcd.line(x2,y2,x3,y3,c)
        self.lcd.line(x3,y3,x1,y1,c)

    def plotWifiIcon(self, status: bool=False, center_x: int=68, center_y: int=68):
        """Plot Wifi icon in screen"""

        if status is None:
            icon_color = self.lcd.orange
        else:
            icon_color = self.lcd.green if status else self.lcd.red

        self.drawCircle(center_x,center_y,35,icon_color)    
        # Down point
        midle_point_y = center_y + 12
        midle_point_radius = 4
        self.drawCircle(center_x, midle_point_y, midle_point_radius, self.lcd.blue)   

        # First half elipse  
        first_half_ellipse_center_y = midle_point_y - 4
        for i in range(4,8):
            self.lcd.ellipse(center_x,first_half_ellipse_center_y, i, i+0, self.lcd.blue, False, 0x03)            

        # Second half elipse  
        second_half_ellipse_center_y = first_half_ellipse_center_y - 5
        for i in range(4,8):
            self.lcd.ellipse(center_x,second_half_ellipse_center_y, i+5, i+2, self.lcd.blue, False, 0x03)  

        # Third half elipse  
        third_half_ellipse_center_y = second_half_ellipse_center_y - 5
        for i in range(4,8):
            self.lcd.ellipse(center_x,third_half_ellipse_center_y, i+10, i+4, self.lcd.blue, False, 0x03)    

    def plotPresenceIcon(self, status: bool=False, center_x: int=172, center_y: int=68):
        """Plot Presence icon in screen"""
        # Plot circle with status color
        if status is None:
            icon_color = self.lcd.orange
        else:
            icon_color = self.lcd.green if status else self.lcd.red

        self.drawCircle(center_x,center_y,35,icon_color)          

        height = 36
        wide = 20
        roof_extra_wide = 8

        p0 = (center_x,center_y-int(wide/2))
        p1 = (center_x+wide,center_y)
        p2 = (center_x+wide-roof_extra_wide,center_y)
        p3 = (p2[0],center_y+int(height/2))
        p4 = (p3[0]-roof_extra_wide ,p3[1])
        p8 = (center_x-wide,center_y)
        p7 = (p8[0]+roof_extra_wide,center_y)
        p6 = (p7[0],p4[1])
        p5 = (p6[0]+roof_extra_wide,p6[1])

        lines = [
            (p0,p1), 
            (p1,p2),
            (p2,p3),
            (p3,p4),
            (p0,p8),
            (p8,p7),
            (p7,p6),
            (p6,p5)
        ]

        for line in lines:
            x1=line[0][0]
            y1=line[0][1]
            x2=line[1][0]
            y2=line[1][1]
            if x1 == x2:
                for i in range(3):
                    self.lcd.line(x1+i, y1, x2+i, y2, self.lcd.blue)
            else:
                for i in range(3):
                    self.lcd.line(x1, y1+i, x2, y2+i, self.lcd.blue)
        
    def plotEmergencyIcon(self, center_x: int = 68, center_y: int = 170):
        """Plot Emergency icon in screen"""
        side=20
        wide=10
        
        self.drawCircle(center_x,center_y,35,self.lcd.gray)   

        #Draw red cross
        self.lcd.rect(center_x-side, center_y-int(wide/2), 2*side, wide,self.lcd.red,True)  
        self.lcd.rect(center_x-int(wide/2), center_y-side, wide, 2*side,self.lcd.red,True)

    def plotElectricityIcon(self, status: bool=False, center_x: int=172, center_y: int=172):
        """Plot Electricity icon in screen"""
        # Plot circle with status color
        if status is None:
            icon_color = self.lcd.orange
        else:
            icon_color = self.lcd.green if status else self.lcd.red

        self.drawCircle(center_x,center_y,35,icon_color)          

        height = 40
        wide = 40
        inner_wide = 15
        very_inner_wide = 3
        inner_height= 8

        p0 = (center_x+very_inner_wide,center_y-int(inner_height/2))
        p3 = (center_x-very_inner_wide,center_y+int(inner_height/2))
        p1 = (center_x+inner_wide,center_y-int(height/2))
        p4 = (center_x-inner_wide,center_y+int(height/2))
        p5 = (center_x+int(wide/2),p0[1])
        p2 = (center_x-int(wide/2),p3[1])

        lines = [
            (p0,p5), 
            (p5,p4),
            (p4,p3),
            (p3,p2),
            (p2,p1),
            (p1,p0),            
        ]

        for line in lines:
            x1=line[0][0]
            y1=line[0][1]
            x2=line[1][0]
            y2=line[1][1]
            if x1 == x2:
                for i in range(3):
                    self.lcd.line(x1+i, y1, x2+i, y2, self.lcd.blue)
            else:
                for i in range(3):
                    self.lcd.line(x1, y1+i, x2, y2+i, self.lcd.blue)

    def plotCrossIcon(self):
        """Plot Cross icon in screen"""

        center_x = 50
        center_y = 100
        side = 40
        
        for i in range(10):
            # Print cross line 1
            x0_a = center_x
            y0_a = center_y+i
            x1_a = center_x+side
            y1_a = center_y+side+i
            self.lcd.line(x0_a,y0_a,x1_a,y1_a,self.lcd.black)
            
            # Print cross line 2
            x0_b = center_x
            y0_b = center_y+side+i
            x1_b = center_x+side
            y1_b = center_y+i
            self.lcd.line(x0_b,y0_b,x1_b,y1_b,self.lcd.black)
            
    def plotTickIcon(self):
        """Plot Tick icon in screen"""

        center_x = 150
        center_y = 120
        side_short = 20
        x_long = 25
        y_long = 2*x_long
        
        for i in range(10):
            # Print short line
            x0_a = center_x
            y0_a = center_y+i
            x1_a = center_x+side_short
            y1_a = center_y+side_short+i
            self.lcd.line(x0_a,y0_a,x1_a,y1_a,self.lcd.black)
            
            # Print long line 
            x0_b = x1_a
            y0_b = y1_a
            x1_b = x0_b+x_long
            y1_b = y0_b-y_long
            self.lcd.line(x0_b,y0_b,x1_b,y1_b,self.lcd.black)  

    def showInitBackground(self):
        """Set Initbackground"""       
        
        self.lcd.fill(self.lcd.black)
        # External circle
        self.drawRing(120,120,120,self.lcd.white)
        self.drawRing(120,120,119,self.lcd.white)
        self.drawRing(120,120,118,self.lcd.white)

        # Separation lines
        self.lcd.rect(120, 0, 3, 240,self.lcd.gray,True)  
        self.lcd.rect(0, 120, 240, 3,self.lcd.gray,True)  
        
        # Plot Wifi Icon
        self.plotWifiIcon(status=self.current_wifi_status)

        # Plot Presence Icon
        self.plotPresenceIcon(status=self.current_presence_status)

        # Plot Emergency Icon
        self.plotEmergencyIcon()

        # Plot Electricity Icon
        self.plotElectricityIcon(status=self.current_electricity_status)

        # Show screen
        self.lcd.show()    
    
    def showConfirmationScreen(self):
        """Set Confirmation screen""" 
        
        # Set background colors
        self.lcd.fill(self.lcd.green)
        self.lcd.rect(0, 0, 119, 239,self.lcd.red,True)

        # Separation lines
        self.lcd.rect(120, 0, 3, 240,self.lcd.gray,True)  

        # Plot cross icon
        self.plotCrossIcon()

        # Plot tick icon
        self.plotTickIcon()

        # Show screen
        self.lcd.show() 

    def showSendingAlarmScreen(self):
        """Set Sending alarm screen"""
        # Set background color
        self.lcd.fill(self.lcd.black)

        # Plot Emergency Icon
        self.plotEmergencyIcon(center_x=120, center_y=160)

        # Plot text
        self.lcd.write_text('Sending',70,40,2,self.lcd.white)
        self.lcd.write_text('alarm',80,80,2,self.lcd.white)

        # Show screen
        self.lcd.show() 
    
    def showSendingCommandScreen(self, ressource: str, new_status: bool):
        """Set Sending alarm screen"""
        # Set background color
        self.lcd.fill(self.lcd.black)       

        # Plot text
        self.lcd.write_text('Sending',70,40,2,self.lcd.white)
        self.lcd.write_text('command',70,80,2,self.lcd.white)

        # Plot Icon
        if ressource == "wifi":
            self.plotWifiIcon(status=new_status, center_x=120, center_y=160)
        if ressource == "presence":
            self.plotPresenceIcon(status=new_status, center_x=120, center_y=160)
        if ressource == "electricity":
            self.plotElectricityIcon(status=new_status, center_x=120, center_y=160)

        # Show screen
        self.lcd.show() 


    def updateWifiStatus(self, wifi_status: bool):
        """Update Wifi status in screen"""
        self.current_wifi_status = wifi_status
        self.plotWifiIcon(status=wifi_status)
        # Show screen
        self.lcd.show() 
    
    def updatePresenceStatus(self, presence_status: bool):
        """Update Presence status in screen"""
        self.current_presence_status=presence_status
        self.plotPresenceIcon(status=presence_status)
        # Show screen
        self.lcd.show() 
    
    def updateElectricalStatus(self, electrical_status: bool):
        """Update Electrical status in screen"""
        self.current_electricity_status=electrical_status
        self.plotElectricityIcon(status=electrical_status)
        # Show screen
        self.lcd.show()         

    def showCurrentStatus(self):
        """Show current status"""
        self.showInitBackground()
        self.updateWifiStatus(wifi_status=self.current_wifi_status)
        self.updatePresenceStatus(presence_status=self.current_presence_status)
        self.updateElectricalStatus(electrical_status=self.current_electricity_status)
    
lcd_manager_service: LCDManager = LCDManager()
""" LCD manager service singleton"""
