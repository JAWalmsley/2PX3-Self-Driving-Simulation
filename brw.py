import random

ARRIVAL = "Arrival"
CLEAR = "Clear"
STOP = "Stop"
LIGHT = "Light"

debug = False


def log(msg):
    out = ''
    if type(msg) == list:
        for m in msg:
            out += str(m) + ' '
    else:
        out = msg
    if (debug):
        print(out)


class Driver():
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.max_stop_time = 10
        self.min_stop_time = 5
        self.max_clear_time = 15
        self.min_clear_time = 10
        self.stop_time = None
        self.clear_time = None

    def get_stop_time(self):
        if (self.stop_time == None):
            self.stop_time = random.randint(
                self.min_stop_time, self.max_stop_time)
        return self.stop_time

    def get_clear_time(self):
        if (self.clear_time == None):
            self.clear_time = random.randint(
                self.min_clear_time, self.max_clear_time)
        return self.clear_time


class SelfDriver(Driver):
    def __init__(self, arrival_time):
        super().__init__(arrival_time)

    def get_stop_time(self):
        return self.min_stop_time

    def get_clear_time(self):
        return self.min_clear_time


class Road():
    def __init__(self):
        self.waiting = []


class Event():
    def __init__(self, start_time: int, type: str, driver: Driver, road: Road, delay: int):
        self.time: int = start_time
        self.type: str = type
        self.driver: Driver = driver
        self.road: Road = road
        self.delay = delay

    def __str__(self):
        return f"E {self.type} {self.time}"


class Simulation:
    def __init__(self, num_arrivals: int, mean_arrival_time: int, light_interval: int, auto_percent: int) -> None:
        self.num_arrivals: int = num_arrivals
        self.mean_arrival_time: int = mean_arrival_time
        self.light_interval = light_interval
        self.auto_percent = auto_percent

        self.events: list[Event] = []
        self.clock = 0
        # 0 = N, 1 = E, 2 = S, 3 = W
        self.roads: list[Road] = [Road(), Road(), Road(), Road()]
        self.lightRoads = [self.roads[0], self.roads[2]]
        self.wait_times = []
        self.populate_events()
        self.skipped_events = 0

    def run(self):
        c = True
        while (len(self.events) > 0 and c):
            c = False
            for e in self.events:
                if not e.type == LIGHT:
                    c = True
                    break
            self.process_events()
        log(self.wait_times)
        return sum(self.wait_times)/len(self.wait_times)

    def process_events(self):
        self.events.sort(key=lambda x: x.time, reverse=True)
        event = self.events[-self.skipped_events - 1]
        log("")
        log(self.clock)
        if (event.type == ARRIVAL):
            self.clock = max(self.clock, event.time) + event.delay
            self.events.remove(event)
            log(f"Arriving with clear time {event.driver.get_clear_time()} on road {self.roads.index(event.road)}")
            event.driver.arrival_time = self.clock
            if (not event.road in self.lightRoads):
                self.events.append(
                    Event(self.clock, STOP, event.driver, event.road, event.driver.get_stop_time()))
            self.events.append(Event(
                self.clock, CLEAR, event.driver, event.road, event.driver.get_clear_time()))

        elif (event.type == CLEAR):
            if (event.road in self.lightRoads):
                self.clock = max(self.clock, event.time) + event.delay
                self.events.remove(event)
                log(f"Driver that arrived at {event.driver.arrival_time} is clearing after waiting {self.clock - event.driver.arrival_time}")
                self.wait_times.append(self.clock - event.driver.arrival_time)
            else:
                log(
                    f"Skipping driver waiting on road {self.roads.index(event.road)}")
                event.road.waiting.append(event.driver)
                self.skipped_events += 1

        elif (event.type == STOP):
            self.clock = max(self.clock, event.time) + event.delay
            self.events.remove(event)
            log(f"Driver that arrived at {event.driver.arrival_time} is stopping")

        elif (event.type == LIGHT):
            self.clock = max(self.clock, event.time) + event.delay
            self.skipped_events = 0
            self.events.remove(event)

            if (self.roads[0] in self.lightRoads):
                log(f"Light change: 1, 3")
                self.lightRoads = [self.roads[1], self.roads[3]]
            else:
                log(f"Light change: 0, 2")
                self.lightRoads = [self.roads[0], self.roads[2]]
            self.events.append(
                Event(self.clock + self.light_interval, LIGHT, None, None, 0))

    def populate_events(self):
        self.events.append(Event(self.light_interval, LIGHT, None, None, 0))
        last_time = 0
        for i in range(self.num_arrivals):
            d = Driver(last_time)
            if (random.randint(0, 100) <= self.auto_percent):
                d = SelfDriver(last_time)
            arrival = Event(last_time,
                            ARRIVAL,
                            Driver(last_time),
                            random.choice(self.roads), 0)
            self.events.append(arrival)
            last_time += int(random.expovariate(1/self.mean_arrival_time))


for i in range(1, 30, 1):
    print(i, ",", end="")
    s = Simulation(1000, i, 20, 0)
    print(s.run())
