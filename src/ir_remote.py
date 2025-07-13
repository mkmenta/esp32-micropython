import machine
import utime

class IRRemote:
    
    def __init__(self, pwm_pin=13, ir_sensor_pin=15, frequency=38000):
        self.pwm = machine.PWM(machine.Pin(pwm_pin))
        self.pwm.freq(frequency)  # Set frequency to 38kHz
        self.pwm.duty(0)  # Start with duty cycle 0 (off)
        self.ir_sensor = (machine.Pin(ir_sensor_pin, machine.Pin.IN)
                          if ir_sensor_pin is not None else None)

    
    def send_ir_signal(self, signal_data, verbose=True):
        """
        Send IR signal using PWM based on the signal data.

        Connection: simply connect the IR LED with a 100ohm resistor to the PWM pin. 
        In my case it needs to be really close to the receiver to work.
        
        Args:
            signal_data (list): List of (timestamp, state) tuples from listen_ir.
        """
        if not signal_data:
            if verbose:
                print("No signal data to send.")
            return
        # Process each state change
        for i in range(len(signal_data) - 1):
            current_time, current_state = signal_data[i]
            next_time, _ = signal_data[i + 1]  
            # Calculate duration for this state
            duration = next_time - current_time
            if current_state == 1:
                # Set PWM duty to 512/1023 (≈50%) for ON state
                self.pwm.duty(512)
            else:
                # Set PWM duty to 0 for OFF state
                self.pwm.duty(0)
            # Wait for the duration before next state change
            if duration > 0:
                utime.sleep_us(duration)
        # Turn off PWM at the end
        self.pwm.duty(0)
        if verbose:
            print("IR signal sent successfully.")
    
    def listen_ir(self, invert=True):
        """
        Listen for IR signals for 2 seconds and record the data.
        Returns a list of (timestamp, state) tuples for plotting.

        Connection: used a VS1838B IR receiver with the circuit in 
        https://docs.keyestudio.com/projects/KS3023/en/latest/MicroPython_Windows/MicroPython.html#project-31-ir-receiver-module
        In this case invert needs to be True, since the sensor returns 0 when detecting a signal.
        
        Args:
            invert (bool): If True, invert the signal (0 becomes 1, 1 becomes 0).
                        This is useful since the sensor returns 0 when detecting a signal.
        """
        assert self.ir_sensor is not None, "IR sensor pin not initialized."
        print("Listening for IR signals for 2 seconds...")
        # Initialize variables
        signal_data = []
        start_time = utime.ticks_us()
        end_time = start_time + 2000000  # 2 seconds in microseconds
        # Get initial state
        raw_state = self.ir_sensor.value()
        prev_state = 1 - raw_state if invert else raw_state
        timestamp = 0
        signal_data.append((timestamp, prev_state))  # Record initial state
        # Record signal for 2 seconds
        while utime.ticks_us() < end_time:
            # Get current state and timestamp
            raw_state = self.ir_sensor.value()
            state = 1 - raw_state if invert else raw_state
            timestamp = utime.ticks_diff(utime.ticks_us(), start_time)
            # Only record when state changes
            if state != prev_state:
                signal_data.append((timestamp, state))
                prev_state = state
            # Small delay for higher precision
            utime.sleep_us(10)
        print("Finished listening.")
        # Print the data for processing on the computer
        if signal_data:
            print("IR Signal Data in us")
        else:
            print("No IR signals detected.")
        init_t = signal_data[1][0] if len(signal_data) > 1 else 0
        signal_data = [(t - init_t, s) for t, s in signal_data[1:]]
        return signal_data
