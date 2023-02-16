import random

# Constants
ARRIVAL = "Arrival"
DEPARTURE = "Departure"
STOP = "Stop"
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


class Event:

    def __init__(self, event_type, time, direction):
        self.type = event_type
        self.time = time
        self.direction = direction


class EventQueue:

    def __init__(self):
        self.events = []

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


class Road:
    def __init__(self, direction):
        self.direction = direction
        self.ready = False


class Simulation:
    def __init__(self, total_arrivals, mean_arrival_time):
        self.num_of_arrivals = 0
        self.num_of_departures = 0
        self.total_arrivals = total_arrivals
        self.upper_arrival_time = 2 * mean_arrival_time
        self.clock = 0
        self.roads = {N: Road("N"),
                      E: Road("E"),
                      S: Road("S"),
                      W: Road("W")}

        self.intersection_free = True
        self.print_events = False
        self.events = EventQueue()
        self.data = []

    def run(self):
        while self.num_of_departures <= self.total_arrivals:
            if self.print_events:
                self.print_state()
            self.execute_next_event()
        self.generate_report()

    def execute_next_event(self):
        event = self.events.get_next_event()
        self.clock = event.time
        if event.type == ARRIVAL:
            self.execute_arrival(event)
        if event.type == DEPARTURE:
            self.execute_departure(event)
        if event.type == STOP:
            self.execute_stop(event)
