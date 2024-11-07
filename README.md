# M/M/S/S Queue Blocking Probability Simulation

This project is a task from the **Advanced Mobile Information Networks** course. It simulates the blocking probability in an M/M/S/S queue system using both theoretical Erlang B formula and Monte Carlo simulation.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Files](#files)
- [License](#license)

## Introduction

The M/M/S/S queue model is used to represent systems with multiple servers and no waiting room. This project calculates the blocking probability, which is the probability that an arriving customer will be blocked (i.e., not served) because all servers are busy.

## Features

- **Erlang B Formula**: Calculates the theoretical blocking probability.
- **Monte Carlo Simulation**: Simulates the blocking probability using random sampling.
- **Interactive Chart**: Plots the theoretical and simulated blocking probabilities for comparison.

## Installation

1. Clone the repository:
  ```sh
  git clone https://github.com/zhaxal/amin-report-one.git
  ```
2. Navigate to the project directory:
  ```sh
  cd amin-report-one
  ```

## Usage

1. Open `index.html` in a web browser.
2. Enter the number of servers (S), arrival rate (λ), and service rate (μ).
3. Click the "Run Simulation" button to see the results.

## Files

- `index.html`: The main HTML file.
- `css/style.css`: The stylesheet for the project.
- `js/chart.js`: Contains the code for plotting the chart.
- `js/simulation.js`: Contains the Monte Carlo simulation code.
- `js/erlangB.js`: Contains the Erlang B formula code.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
