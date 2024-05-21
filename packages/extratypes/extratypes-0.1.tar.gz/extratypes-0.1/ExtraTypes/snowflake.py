import sys, threading, time

class snowflake:
    def __init__(self, value: str=None):
        self.value = None
        self.sequence = 0
        self.epoch = 1609459200  # Unix-Zeitstempel: 1. Januar 2021, 00:00:00 UTC
        self.machine_id = 0
        self.lock = threading.Lock()
        if not value:
            self.value = self.generate_id()
            return

        if isinstance(value, str):
            if value.isnumeric():
                value = int(value)
            else:
                raise ValueError("Input is not a valid Snowflake ID. Input is not numeric.")


        if isinstance(value, int) and -sys.maxsize - 1 <= value <= sys.maxsize:
            self.value = value

        else:
            raise ValueError("Input is not a valid Snowflake ID.")
        
    def generate_id(self):
        with self.lock:
            timestamp = int(time.time()) - self.epoch
            snowflake_id = (timestamp << 22) | (self.machine_id << 12) | self.sequence
            self.sequence = (self.sequence + 1) & 4095  # 12 bits für die Sequenznummer (0-4095)
        return snowflake_id


    def __str__(self):

        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, snowflake):
            return self.value == other.value
        elif isinstance(other, str):
            return str(self.value) == other
        elif isinstance(other, int):
            print("Not suposed to compare snowflake with int. Compare with snowflake or str instead.")
            return False
        else:
            return False

    def __hash__(self):
        return hash(self.value)
    
if __name__ != "__main__":	
    globals().update(snowflake.__dict__)