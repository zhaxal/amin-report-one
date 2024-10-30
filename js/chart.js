let chartInstance = null; // Store chart instance

function simulateAndPlot() {
  const servers = parseInt(document.getElementById("servers").value);
  const lambda = parseFloat(document.getElementById("lambda").value);
  const mu = parseFloat(document.getElementById("mu").value);

  // Calculate offered loads based on lambda and mu
  const offeredLoads = Array.from(
    { length: 20 },
    (_, i) => ((i + 1) * 0.5 * lambda) / mu
  );

  // Calculate theoretical blocking probabilities using Erlang B formula
  const theoreticalBlocking = offeredLoads.map((A) =>
    erlangBFormula(A, servers)
  );

  // Simulate blocking probabilities using Monte Carlo method
  const simulatedBlocking = offeredLoads.map(() =>
    simulateBlockingProbability(lambda, mu, servers, 1000)
  );

  const ctx = document.getElementById("chart").getContext("2d");

  // Destroy the existing chart instance if it exists
  if (chartInstance) {
    chartInstance.destroy();
  }

  // Create a new chart instance and store it in chartInstance
  chartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: offeredLoads,
      datasets: [
        {
          label: "Erlang B Formula",
          data: theoreticalBlocking,
          borderColor: "blue",
          fill: false,
        },
        {
          label: "Simulation",
          data: simulatedBlocking,
          borderColor: "red",
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: "Offered Load (A)",
          },
        },
        y: {
          title: {
            display: true,
            text: "Blocking Probability",
          },
          beginAtZero: true,
        },
      },
    },
  });
}
