import time
from managers.thread import thread_manager_service
from managers.lcd import lcd_manager_service
from managers.touch import touch_manager_service

enable_status_update = False
ALARM_MSG = "~al_bt_em #"
COMMANDS = {
   "wifi": {
      True: "wifi_all-on ",
      False: "wifi_all-off "
   },
   "presence": {
      True: "us_PRESENCE-DAY-LOW-CONSUMPTION ",
      False: "us_ABSENCE-LOW-CONSUMPTION "
   },
   "electricity": {
      True: "ep_111111 ",
      False: "ep_000000 "
   },
}

def thread_msg_callback(msg):
    global enable_status_update

    message = msg.decode("utf-8")

    if enable_status_update:
        # Check if wifi status in message
        if "wifi" in message:
            _status = message.split("wifi:")[1][0]
            wifi_status = True if _status == '1' else False
            lcd_manager_service.updateWifiStatus(wifi_status=wifi_status)
        
        # Check if presence status in message
        if "prs" in message:
            _status = message.split("prs:")[1][0]
            prs_status = True if _status == '1' else False
            lcd_manager_service.updatePresenceStatus(presence_status=prs_status)
        
        # Check if electrical status in message
        if "ele" in message:
            _status = message.split("ele:")[1][0]
            electrical_status = True if _status == '1' else False
            lcd_manager_service.updateElectricalStatus(electrical_status=electrical_status)
    else:
        print("Status update disabled")


def main():
    global enable_status_update
    
    # Setup LCD manager
    lcd_manager_service.setup(brightness=65535)

    # Setup Touch manager
    touch_manager_service.setup(LCD=lcd_manager_service, mode=1)

    # Setup thread manager
    thread_manager_service.setup_thread_interface(
        baudrate= 115200,
        bits = 8,
        parity = None,
        stop = 1,
        tx_pin = 16,
        rx_pin = 17,
        msg_callback=thread_msg_callback,
    )

    enable_status_update = True
    
    while True:              
        
        button_pressed = touch_manager_service.waitForTouch()
        print(f"Button pressed: {button_pressed}")
        enable_status_update = False
        confirmation=False

        # Show confirmation screen
        lcd_manager_service.showConfirmationScreen()

        # Wait for swipe
        new_status = touch_manager_service.waitForSwipe()

        if button_pressed == 3 and new_status:
            # Send alarm
            print("sending alarm")
            thread_manager_service.send_thread_message_to_border_router(message=ALARM_MSG)
            # Show sending command Screen
            lcd_manager_service.showSendingAlarmScreen()
            time.sleep(10) 

        else:    
            # Show sending command Screen
            if button_pressed == 1:
                ressource = "wifi"
                old_status = lcd_manager_service.current_wifi_status
            if button_pressed == 2:
                ressource = "presence"
                old_status = lcd_manager_service.current_presence_status
            if button_pressed == 4:
                ressource = "electricity"
                old_status = lcd_manager_service.current_electricity_status
            
            if new_status != old_status:
                # Get command
                command=COMMANDS[ressource][new_status]
                print(f"Sending command for ressource {ressource}  new_status:{new_status}  command: {command}")
                command = f"~{command}#"
                thread_manager_service.send_thread_message_to_border_router(message=command)
                lcd_manager_service.showSendingCommandScreen(ressource=ressource, new_status=new_status)
                time.sleep(10)          

        # Show init background
        enable_status_update = True
        lcd_manager_service.showCurrentStatus()
        

if __name__ == '__main__':
    main()