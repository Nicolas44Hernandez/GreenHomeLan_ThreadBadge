from interfaces.thread_dongle import ThreadDongleInterface


class ThreadManager:
    """Manager for thread interface"""

    thread_interface: ThreadDongleInterface
    #TODO: How to send keep alive (separated thread?)
    keep_alive_message_period_in_secs: int
    device_id: int

    def setup_thread_interface(
            self, 
            baudrate: int=115200,
            bits: int= 8,
            parity: int= None,
            stop: int= 1,
            tx_pin: int= 16,
            rx_pin: int= 17,
            msg_callback: callable=None,

        ):
        # Create Thread interface

        self.thread_interface = ThreadDongleInterface(
            baudrate=baudrate,
            bits=bits,
            parity=parity,
            stop=stop,
            tx_pin=tx_pin,
            rx_pin=rx_pin,
        )

        # Set message reception callback
        self.thread_interface.set_msg_reception_callback(msg_callback)

        # Run thread donfgle interface in dedicated thread
        self.thread_interface.run_dedicated_thread()

        # Run thread donfgle interface in dedicated thread
        self.thread_interface.run_dedicated_thread()


    def send_thread_message_to_border_router(self, message: str):
        """Send message to border router"""

        msg = f"{message} "

        if not self.thread_interface.send_message_to_border_router(msg=msg):
            print(
                "[ERROR] Thread network not configured or not running, wating for network setup message"
            )
            print("[ERROR] Message not published")


thread_manager_service: ThreadManager = ThreadManager()
""" Thread manager service singleton"""
