import machine
import utime

class IRRemote:
    
    def __init__(self, pwm_pin=13, frequency=38000):
        self.pwm = machine.PWM(machine.Pin(pwm_pin))
        self.pwm.freq(frequency)  # Set frequency to 38kHz
        self.pwm.duty(0)  # Start with duty cycle 0 (off
    
    def send_ir_signal(self, signal_data, verbose=True):
        """
        Send IR signal using PWM based on the signal data.
        
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
