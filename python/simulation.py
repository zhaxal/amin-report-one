import numpy as np
import matplotlib.pyplot as plt
from math import factorial
from typing import List, Tuple
from collections import deque

def erlang_b_formula(A: float, S: int) -> float:
    """
    Calculate blocking probability using Erlang B formula.
    
    Args:
        A (float): Offered load
        S (int): Number of servers
    
    Returns:
        float: Blocking probability
    """
    try:
        numerator = (A ** S) / factorial(S)
        denominator = sum((A ** k) / factorial(k) for k in range(S + 1))
        return numerator / denominator
    except OverflowError:
        # Handle large numbers more efficiently
        log_numerator = S * np.log(A) - np.log(factorial(S))
        log_denominator = np.log(sum((A ** k) / factorial(k) for k in range(S + 1)))
        return np.exp(log_numerator - log_denominator)

def simulate_blocking_probability(lambda_: float, mu: float, servers: int, 
                               simulation_time: float) -> Tuple[float, int]:
    """
    Simulate M/M/S/S queue using discrete event simulation.
    
    Args:
        lambda_: Arrival rate
        mu: Service rate
        servers: Number of servers
        simulation_time: Total simulation time
    
    Returns:
        Tuple[float, int]: (Blocking probability, Total arrivals)
    """
    class Event:
        def __init__(self, time: float, event_type: str):
            self.time = time
            self.type = event_type
        
        def __lt__(self, other):
            return self.time < other.time

    # Initialize simulation variables
    current_time = 0.0
    servers_in_use = 0
    total_arrivals = 0
    blocked_arrivals = 0
    
    # Priority queue for events
    events = []
    
    # Schedule first arrival
    events.append(Event(np.random.exponential(1/lambda_), "arrival"))
    
    # Run simulation
    while current_time < simulation_time:
        if not events:
            # If no events, generate new arrival
            next_time = current_time + np.random.exponential(1/lambda_)
            if next_time < simulation_time:
                events.append(Event(next_time, "arrival"))
            continue
        
        # Get next event
        events.sort()  # Sort by time
        event = events.pop(0)
        current_time = event.time
        
        if current_time > simulation_time:
            break
            
        if event.type == "arrival":
            # Handle arrival
            total_arrivals += 1
            
            # Schedule next arrival
            next_arrival = current_time + np.random.exponential(1/lambda_)
            if next_arrival < simulation_time:
                events.append(Event(next_arrival, "arrival"))
            
            if servers_in_use < servers:
                # Service can start
                servers_in_use += 1
                # Schedule departure
                service_time = np.random.exponential(1/mu)
                events.append(Event(current_time + service_time, "departure"))
            else:
                # All servers busy - request blocked
                blocked_arrivals += 1
                
        else:  # departure
            servers_in_use = max(0, servers_in_use - 1)
    
    # Ensure minimum number of arrivals for statistical significance
    min_arrivals = 10000
    if total_arrivals < min_arrivals:
        return simulate_blocking_probability(lambda_, mu, servers, simulation_time * 2)
    
    blocking_prob = blocked_arrivals / total_arrivals if total_arrivals > 0 else 0
    return blocking_prob, total_arrivals

def run_simulation(servers: int, lambda_: float, mu: float) -> tuple[List[float], List[float], List[float]]:
    """
    Run simulation and calculate both theoretical and simulated blocking probabilities.
    
    Args:
        servers (int): Number of servers
        lambda_ (float): Base arrival rate
        mu (float): Service rate
    
    Returns:
        tuple: Lists of offered loads, theoretical blocking probs, and simulated blocking probs
    """
    # Calculate offered loads
    offered_loads = [(i + 1) * 0.5 for i in range(40)]  # More data points
    
    # Calculate theoretical blocking probabilities
    print("\nCalculating theoretical probabilities...")
    theoretical_blocking = [erlang_b_formula(A, servers) for A in offered_loads]
    
    # Simulate blocking probabilities
    print("Running simulation...")
    simulated_blocking = []
    total_samples = []
    
    for i, A in enumerate(offered_loads):
        # Adjust arrival rate to maintain desired offered load A
        adjusted_lambda = A * mu
        
        # Run multiple iterations for each load point to get better average
        num_iterations = 5
        probs = []
        for _ in range(num_iterations):
            prob, samples = simulate_blocking_probability(adjusted_lambda, mu, servers, 20000)
            probs.append(prob)
            
        avg_prob = np.mean(probs)
        simulated_blocking.append(avg_prob)
        print(f"Progress: {i+1}/{len(offered_loads)} simulations complete")
    
    return offered_loads, theoretical_blocking, simulated_blocking

def plot_results(offered_loads: List[float], theoretical: List[float], simulated: List[float]) -> None:
    """
    Plot the comparison between theoretical and simulated results.
    
    Args:
        offered_loads (List[float]): List of offered loads
        theoretical (List[float]): List of theoretical blocking probabilities
        simulated (List[float]): List of simulated blocking probabilities
    """
    plt.figure(figsize=(12, 8))
    plt.plot(offered_loads, theoretical, 'b-', label='Erlang B Formula', linewidth=2)
    plt.plot(offered_loads, simulated, 'r--', label='Simulation', linewidth=2)
    plt.xlabel('Offered Load (A)', fontsize=12)
    plt.ylabel('Blocking Probability', fontsize=12)
    plt.title('M/M/S/S Queue Blocking Probability', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    """Main function to run the simulation application."""
    print("M/M/S/S Queue Blocking Probability Simulation")
    print("--------------------------------------------")
    
    # Get user input
    while True:
        try:
            servers = int(input("\nEnter number of servers (S): "))
            lambda_ = float(input("Enter arrival rate (λ): "))
            mu = float(input("Enter service rate (μ): "))
            
            if servers <= 0 or lambda_ <= 0 or mu <= 0:
                raise ValueError("All values must be positive")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
    
    # Run simulation and plot results
    offered_loads, theoretical, simulated = run_simulation(servers, lambda_, mu)
    plot_results(offered_loads, theoretical, simulated)

if __name__ == "__main__":
    main()