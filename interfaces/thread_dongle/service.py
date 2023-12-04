"""
Thread dongle interface service
"""
import time
import _thread
from machine import Pin,UART
import time

class ThreadClientDongle():
    """Service class for thread client management"""

    thread_serial_port: str
    uart_interface: UART
    msg_reception_callback: callable

    def __init__(
            self, 
            baudrate: int = 115200, 
            bits: int =8, 
            parity: int=None, 
            stop: int=1,
            tx_pin: int=16, 
            rx_pin: int = 17
        ):
        
        print(f"Creatting UART interface object...")
        self.uart_interface = UART(
            0, 
            baudrate=baudrate, 
            bits=bits, 
            parity=parity, 
            stop=stop, 
            tx=Pin(tx_pin), 
            rx=Pin(rx_pin)
        )

        self.msg_reception_callback = None


    def run_dedicated_thread(self):
        """Run Thread loop in dedicated if network is setted up"""
        print(f"Running Thread loop in dedicated thread")
        try:
            _thread.start_new_thread(self.run, ())
        except Exception as e:
            print(e)

    def run(self):
        """Run thread"""        

        while True:
            if self.uart_interface.any(): 
                data = self.uart_interface.read()
                if self.msg_reception_callback is None :
                    print("Callback is None")
                    continue
                if len(data) < 4 :
                    print("data len < 4")
                    continue
                self.msg_reception_callback(data)
            time.sleep(0.1)

    def send_message_to_border_router(self, msg: str):
        """Send thread message to Border router"""

        print("Sending message ", msg)
        ret  = self.uart_interface.write(msg)
        print("ret message ", ret)
        # TODO: when should we return False ?
        while not self.uart_interface.txdone():
            time.sleep(0.1)
            print("waiting data to be sent")
        return True

    def set_msg_reception_callback(self, callback: callable):
        """Set msg reception callback"""
        self.msg_reception_callback = callback