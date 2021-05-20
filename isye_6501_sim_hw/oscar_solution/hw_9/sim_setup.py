import random
import simpy
from typing import List, Optional, Dict


class AirportSecuritySystem(object):
    """A simplified airport security system at a busy airport has check each passenger
    in two steps.

    First, they have to pass through the ID/boarding-pass check queue, where there are
    limited number of servers. After that, the passengers are assigned to the shortest
    of the several personal-check queues, where they go through the personal scanner
    """
    def __init__(self,
                 env,
                 num_id_check_stands,
                 num_scanner_stands,
                 mean_id_check_time,
                 scanner_time_params,
                 ):

        self.env = env
        self.id_check_stand = simpy.Resource(env, num_id_check_stands)
        self.scanner_stand = simpy.Resource(env, num_scanner_stands)
        self.mean_id_check_time = mean_id_check_time
        self.scanner_time_params: List[float] = scanner_time_params

    def id_check(self, passenger_name, debug=False):
        """The ID/boarding-pass process."""
        rand_id_check_time = random.expovariate(1 / self.mean_id_check_time)

        yield self.env.timeout(rand_id_check_time)
        print(f"Checking ID of passenger {passenger_name}") if debug else None

    def scanner_check(self, passenger_name, debug=False):
        """The personal scanner check"""
        rand_scan_time = random.uniform(*self.scanner_time_params)

        yield self.env.timeout(rand_scan_time)
        print(f"Scan check of passenger: {passenger_name}") if debug else None


def security_check(env,
                   passenger_name,
                   airport_check: AirportSecuritySystem,
                   results: Optional[Dict[str, list]] = None,
                   debug: bool = False):

    """The passenger process, each passenger has a name.

    The passenger first enters the ID check and then the scanner check
    """
    # In this code we use the "with" statement that  tells the simulation to
    # automatically release the resource once the process is complete
    # This can also be accomplished with the release() method on the environment if done
    # manually

    arrival_time = env.now
    print(f"{passenger_name} arrives at the airport at {arrival_time}") if debug else None

    with airport_check.id_check_stand.request() as id_check_request:
        yield id_check_request
        start_id_check = env.now
        print(f"{passenger_name} enters the ID Check at {start_id_check}") if debug else None

        yield env.process(airport_check.id_check(passenger_name, debug))

        id_check_time = env.now - start_id_check
        print(f"{passenger_name} leaves ID Check at {env.now}") if debug else None

    with airport_check.scanner_stand.request() as scan_request:
        yield scan_request

        start_scan_check = env.now
        print(f"{passenger_name} enter the Personal Scan at {start_scan_check}") if debug else None

        yield env.process(airport_check.scanner_check(passenger_name, debug))

        scanner_check_time = env.now - start_scan_check
        print(f"{passenger_name} leaves the Personal Scan at {env.now}") if debug else None

    # We accept an empty dictionary to store the results of each passenger
    if isinstance(results, dict):
        total_time = env.now - arrival_time
        wait_time = total_time - id_check_time - scanner_check_time
        results["elapsed_time"].append(env.now)
        results["passenger_name"].append(passenger_name)
        results["wait_time"].append(wait_time)
        results["total_time"].append(total_time)
        results["id_check_time"].append(id_check_time)
        results["scanner_check_time"].append(scanner_check_time)
        results["arrival_time"].append(arrival_time)


def run_airport_check(env,
                      num_id_check_stands,
                      num_scanner_stands,
                      mean_id_check_time,
                      scanner_time_params,
                      t_inter,
                      results: Optional[Dict[str, list]] = None,
                      debug: bool = False):

    """Create an airport security check, a number of initial passengers and keep
    the passengers arriving approx. every ``t_inter`` minutes."""

    # Create the airport security check
    airport_sec_check = AirportSecuritySystem(env,
                                              num_id_check_stands,
                                              num_scanner_stands,
                                              mean_id_check_time,
                                              scanner_time_params)

    # Initialize passengers count
    i = 0

    # Keep passengers coming
    while True:
        yield env.timeout(random.expovariate(1 / t_inter))
        i += 1
        env.process(security_check(env,
                                   f"Passenger_{i}",
                                   airport_sec_check,
                                   results,
                                   debug))


# Defining a function to run the simulation to make the code more readable
def run_sim(num_id_check_stands: float,
            num_scanner_stands: float,
            mean_id_check_time: float,
            max_time_scan: List[float],
            interarrival_time: float,
            sim_time: float,
            results: dict = None,
            debug: bool = True):

    # Create an environment and start the setup process
    env = simpy.Environment()
    env.process(run_airport_check(env,
                                  num_id_check_stands,
                                  num_scanner_stands,
                                  mean_id_check_time,
                                  max_time_scan,
                                  interarrival_time,
                                  results,
                                  debug=debug))

    env.run(until=sim_time)
