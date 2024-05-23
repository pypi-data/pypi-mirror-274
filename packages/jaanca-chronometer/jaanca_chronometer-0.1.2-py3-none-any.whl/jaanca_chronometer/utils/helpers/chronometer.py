import time

class Interval:
    '''Format: HH:mm:ss
    '''
    def __init__(self,hours:int=0, minutes:int=0, seconds:int=0) -> None:
        self.hours=hours
        self.minutes=minutes
        self.seconds=seconds
    def __repr__(self) -> str:
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"

class Chronometer:
    def __init__(self) -> None:
        self.reset()
    def start(self)->None:
        '''Start the stopwatch
        '''
        self.reset()
        self.__start_time = time.time()
    def stop(self)->None:
        '''End stopwatch
        '''
        self.__end_time = time.time()
    def reset(self)->None:
        '''Set the stopwatch to zero
        '''
        self.__start_time=0
        self.__end_time=0
    def get_elapsed_time(self)->Interval:
        '''Descripcion
        :return Interval(str): HH:mm:ss format supported for inserting records into databases and adding elapsed times

        ## Example
        ```Python
        from jaanca_chronometer import Chronometer
        import time

        chronometer=Chronometer()
        chronometer.start()
        time.sleep(140)
        chronometer.stop()
        elapsed_time=str(chronometer.get_elapsed_time())
        print(elapsed_time)        
        ´´´
        '''
        elapsed_seconds = self.__end_time - self.__start_time
        hours = int(elapsed_seconds / 3600)
        minutes = int((elapsed_seconds % 3600) / 60)
        seconds = int(elapsed_seconds % 60)
        return Interval(hours, minutes, seconds)

    def get_format_time(self)->str:
        return "HH:mm:ss"