// simulation.js
function simulateBlockingProbability(lambda, mu, servers, timeLimit) {
  let blocked = 0,
    served = 0,
    currentTime = 0,
    serversInUse = 0;
  while (currentTime < timeLimit) {
    let interArrival = -Math.log(Math.random()) / lambda;
    let serviceTime = -Math.log(Math.random()) / mu;
    currentTime += interArrival;

    if (serversInUse < servers) {
      serversInUse++;
      served++;
      setTimeout(() => {
        serversInUse--;
      }, serviceTime * 1000);
    } else {
      blocked++;
    }
  }
  return blocked / (blocked + served);
}
