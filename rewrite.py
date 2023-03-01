import random

# Constants
ARRIVAL = "Arrival"
DEPARTURE = "Departure"
STOP = "Stop"
CLEAR = "Clear"
N = "North"
E = "East"
S = "South"
W = "West"


class Driver:

    min_stop_time = 3
    max_stop_time = 7

    min_clear_time = 7
    max_clear_time = 12

    def __init__(self, name, arrival_time):
        self.name = name
        self.arrival_time = arrival_time

    # Returns driver instance stop time
    def get_stop_time(self):
        return random.uniform(self.min_stop_time, self.max_stop_time)

    # Returns driver instance clear time
    def get_clear_time(self):
        return random.uniform(self.min_clear_time, self.max_clear_time)


class SelfDriver(Driver):
    def get_stop_time(self):
        return self.min_stop_time

    def get_clear_time(self):
        return self.min_clear_time


class Road:
    def __init__(self, direction):
        self.direction: str = direction
        self.ready: bool = False
        self.waiting_cars: list[Driver] = []


class Event:
    def __init__(self, event_type: str, road: Road, driver: Driver, time: int):
        self.event_type: str = event_type
        self.road: Road = road
        self.driver = Driver
        self.time = time


class EventQueue:

    def __init__(self):
        self.events: list[Event] = []

    # Add event (will get sent to the back of the queue)
    def add_event(self, event):
        # print("Adding event: " + event.type + ", clock: " + str(event.time))
        self.events.append(event)

    # Get the next event in the queue and pop it (remove it)
    # Returns removed next event
    def get_next_event(self):
        min_time = 9999999999999
        min_index = 0
        for i in range(len(self.events)):
            if self.events[i].time < min_time:
                min_time = self.events[i].time
                min_index = i
        event = self.events.pop(min_index)
        # print("Removing event: " + event.type + ", clock: " + str(event.time))
        return event


class Simulation:
    def __init__(self, num_arrivals, mean_arrival_time):
        self.num_arrivals = num_arrivals
        self.mean_arrival_time = mean_arrival_time
        self.roads = [Road(N), Road(E), Road(S), Road(W)]
        self.clock = 0
        self.intersection_clear = True
        self.event_queue = EventQueue()
        self.generate_events()
    
    def run(self):
        self.event_queue.sort(key=lambda x: x.time)
        event: Event = self.event_queue.get_next_event()
        if(event.event_type == ARRIVAL):
            if(self.intersection_clear):
                self.intersection_clear = False
                self.event_queue.add_event(Event(CLEAR, event.road, event.driver, self.clock + event.driver.get_clear_time()))
            else:
                event.driver.arrival_time = self.clock
                self.event_queue.add_event(Event(STOP, event.road, event.driver, self.clock + event.driver.get_stop_time()))
                event.road.waiting_cars.append(event.driver)
            
    
    def generate_events(self):
        next_arrival_time = 0
        for i in range(self.num_arrivals):
            next_arrival_time += random.expovariate(1 / self.mean_arrival_time)
            self.event_queue.add_event(Event(ARRIVAL, random.randrange(self.roads), Driver("Driver " + str(i), next_arrival_time)))
        
        


s = Simulation(10000, 10)
s.run()
