"""
    Cookie Clicker Simulator
    """

import simpleplot
import math
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
        Simple class to keep track of the game state.
        """
    
    def __init__(self):
        """
            initiate game state
            """
        self._total_cookies = 0.0
        self._current_time = 0.0
        self._current_cookies = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
    
    def __str__(self):
        """
            Return human readable state
            """
        dummy = 'total cookies: ' + str(self._total_cookies) + '\n' + 'current cookies: ' + str(self._current_cookies) +'\n'+ 'current_cps: ' + str(self._current_cps) + '\n'+ str(len(self._history)) + str(self._history)
        
        return dummy
    
    def get_cookies(self):
        """
            Return current number of cookies
            (not total number of cookies)
            
            Should return a float
            """
        return self._current_cookies
    
    def get_cps(self):
        """
            Get current CPS
            
            Should return a float
            """
        return self._current_cps
    
    def get_time(self):
        """
            Get current time
            
            Should return a float
            """
        return self._current_time
    
    def get_history(self):
        """
            Return history list
            
            History list should be a list of tuples of the form:
            (time, item, cost of item, total cookies)
            
            For example: [(0.0, None, 0.0, 0.0)]
            
            Should return a copy of any internal data structures,
            so that they will not be modified outside of the class.
            """
        return list(self._history)
    
    def time_until(self, cookies):
        """
            Return time until you have the given number of cookies
            (could be 0.0 if you already have enough cookies)
            
            Should return a float with no fractional part
            """
        if self._current_cookies >= cookies:
            time = 0.0
        else:
            time = math.ceil((cookies - self._current_cookies) / self._current_cps)
        return time
    
    def wait(self, time):
        """
            Wait for given amount of time and update state
            
            Should do nothing if time <= 0.0
            """
        if time > 0:
            self._total_cookies += self._current_cps * time
            self._current_cookies += self._current_cps * time
            self._current_time += time
    
    
    def buy_item(self, item_name, cost, additional_cps):
        """
            Buy an item and update state
            
            Should do nothing if you cannot afford the item
            """
        if cost <= self._current_cookies:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, item_name, cost, self._total_cookies))


def simulate_clicker(build_info, duration, strategy):
    """
        Function to run a Cookie Clicker game for the given
        duration with the given strategy.  Returns a ClickerState
        object corresponding to the final state of the game.
        """
    
    my_build_info = build_info.clone()
    clicker = ClickerState()
    
    while clicker.get_time() <= duration:
        if strategy(clicker.get_cookies(), clicker.get_cps(), clicker.get_history(), duration - clicker.get_time(), my_build_info) == None:
            break
        elif strategy(clicker.get_cookies(), clicker.get_cps(), clicker.get_history(), duration - clicker.get_time(), my_build_info) == 'Cursor':
            item = 'Cursor'
            cost = my_build_info.get_cost(item)
            time = clicker.time_until(cost)
            if clicker.get_time() + time > duration:
                break
            else:
                clicker.wait(time)
                clicker.buy_item(item, cost, my_build_info.get_cps(item))
                my_build_info.update_item(item)
                while clicker.get_cookies() > my_build_info.get_cost(item):
                    clicker.buy_item(item, my_build_info.get_cost(item), my_build_info.get_cps(item))
                    my_build_info.update_item(item)
        
        else:
            item = strategy(clicker.get_cookies(), clicker.get_cps(), clicker.get_history(), duration - clicker.get_time(), my_build_info)
            cost = my_build_info.get_cost(item)
            time = clicker.time_until(cost)
            clicker.wait(time)
            clicker.buy_item(item, cost, my_build_info.get_cps(item))
            my_build_info.update_item(item)
            while clicker.get_cookies() > my_build_info.get_cost(item):
                clicker.buy_item(item, my_build_info.get_cost(item), my_build_info.get_cps(item))
                my_build_info.update_item(item)
    
    time_left = duration - clicker.get_time()
    clicker.wait(time_left)
    return clicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
        Always pick Cursor!
        
        Note that this simplistic (and broken) strategy does not properly
        check whether it can actually buy a Cursor in the time left.  Your
        simulate_clicker function must be able to deal with such broken
        strategies.  Further, your strategy functions must correctly check
        if you can buy the item in the time left and return None if you
        can't.
        """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
        Always return None
        
        This is a pointless strategy that will never buy anything, but
        that you can use to help debug your simulate_clicker function.
        """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
        Always buy the cheapest item you can afford in the time left.
        """
    items = build_info.build_items()
    #print items
    cheap = None
    cheap_item = None
    for item in items:
        cost = build_info.get_cost(item)
        if cheap == None:
            cheap = cost
            cheap_item = item
        elif cheap > cost:
            cheap = cost
            cheap_item = item
    
    if cookies >= cheap:
        return cheap_item
    elif (cheap - cookies) / cps > time_left:
        return None
    else:
        return cheap_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
        Always buy the most expensive item you can afford in the time left.
        """
    items = build_info.build_items()
    can_make = cookies + time_left * cps
    cost = []
    for item in items:
        cost.append(build_info.get_cost(item))
    if min(cost) > can_make:
        return None
    elif max(cost) <= can_make:
        for item in items:
            if max(cost) == build_info.get_cost(item):
                return item
    else:
        exp = min(cost)
        exp_item = None
        for item in items:
            if min(cost) == build_info.get_cost(item):
                exp_item = item
        for item in items:
            cost = build_info.get_cost(item)
            if cost < can_make and cost > exp:
                exp = cost
                exp_item = item
        return exp_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
        The best strategy that you are able to implement.
        """
    return None

def run_strategy(strategy_name, time, strategy):
    """
        Run a simulation for the given time with one strategy.
        """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

# Plot total cookies over time

# Uncomment out the lines below to see a plot of total cookies vs. time
# Be sure to allow popups, if you do want to see it

# history = state.get_history()
# history = [(item[0], item[3]) for item in history]
# simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
        Run the simulator.
        """
    #run_strategy("Cursor", SIM_TIME, strategy_expensive)
    
    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
# run_strategy("Best", SIM_TIME, strategy_best)

run()


