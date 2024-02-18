from datetime import datetime, timedelta


class CircuitBreaker:
    def __init__(self, error_threshold):
        self.error_threshold = error_threshold
        self._last_error_dt = None
        self._errors = 0
        self.state = "close"

    def half_open(self):
        self._errors = int(self.error_threshold) / 2
        self.state = "half_open"

    def close(self):
        print("close CircuitBreaker")
        self._errors = 0
        self.state = "close"

    def open(self):
        print("open CircuitBreaker")
        self.state = "open"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self._errors += 1
            if self._errors >= self.error_threshold:
                self.open()
                self._last_error_dt = datetime.now()
            return True
        else:
            if self._last_error_dt and datetime.now() > self._last_error_dt + timedelta(seconds=10):
                self.close()
