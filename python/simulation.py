import numpy as np
import matplotlib.pyplot as plt
from math import factorial
import time
from typing import List

def erlang_b_formula(A: float, S: int) -> float:
    """
    Calculate blocking probability using Erlang B formula.
    
    Args:
        A (float): Offered load
        S (int): Number of servers
    
    Returns:
        float: Blocking probability
    """
    numerator = (A ** S) / factorial(S)
    denominator = sum((A ** k) / factorial(k) for k in range(S + 1))
    return numerator / denominator

def simulate_blocking_probability(lambda_: float, mu: float, servers: int, time_limit: float) -> float:
    """
    Simulate M/M/S/S queue to calculate blocking probability.
    
    Args:
        lambda_ (float): Arrival rate
        mu (float): Service rate
        servers (int): Number of servers
        time_limit (float): Simulation time limit
    
    Returns:
        float: Simulated blocking probability
    """
    blocked = 0
    served = 0
    current_time = 0
    servers_in_use = 0
    service_completion_times = []
    
    while current_time < time_limit:
        # Generate next arrival
        inter_arrival = np.random.exponential(1/lambda_)
        current_time += inter_arrival
        
        # Clean up completed services
        while service_completion_times and service_completion_times[0] <= current_time:
            service_completion_times.pop(0)
            servers_in_use -= 1
        
        if servers_in_use < servers:
            # Server available
            served += 1
            servers_in_use += 1
            service_time = np.random.exponential(1/mu)
            service_completion_times.append(current_time + service_time)
            service_completion_times.sort()
        else:
            # All servers busy - request blocked
            blocked += 1
    
    return blocked / (blocked + served) if (blocked + served) > 0 else 0

def run_simulation(servers: int, lambda_: float, mu: float) -> tuple[List[float], List[float], List[float]]:
    """
    Run simulation and calculate both theoretical and simulated blocking probabilities.
    
    Args:
        servers (int): Number of servers
        lambda_ (float): Arrival rate
        mu (float): Service rate
    
    Returns:
        tuple: Lists of offered loads, theoretical blocking probs, and simulated blocking probs
    """
    # Calculate offered loads
    offered_loads = [(i + 1) * 0.5 * lambda_ / mu for i in range(20)]
    
    # Calculate theoretical blocking probabilities
    theoretical_blocking = [erlang_b_formula(A, servers) for A in offered_loads]
    
    # Simulate blocking probabilities
    print("\nRunning simulation...")
    simulated_blocking = []
    for i, _ in enumerate(offered_loads):
        prob = simulate_blocking_probability(lambda_, mu, servers, 1000)
        simulated_blocking.append(prob)
        print(f"Progress: {i+1}/20 simulations complete")
    
    return offered_loads, theoretical_blocking, simulated_blocking

def plot_results(offered_loads: List[float], theoretical: List[float], simulated: List[float]) -> None:
    """
    Plot the comparison between theoretical and simulated results.
    
    Args:
        offered_loads (List[float]): List of offered loads
        theoretical (List[float]): List of theoretical blocking probabilities
        simulated (List[float]): List of simulated blocking probabilities
    """
    plt.figure(figsize=(10, 6))
    plt.plot(offered_loads, theoretical, 'b-', label='Erlang B Formula')
    plt.plot(offered_loads, simulated, 'r--', label='Simulation')
    plt.xlabel('Offered Load (A)')
    plt.ylabel('Blocking Probability')
    plt.title('M/M/S/S Queue Blocking Probability')
    plt.legend()
    plt.grid(True)
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