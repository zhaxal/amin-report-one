// erlangB.js
function erlangBFormula(A, S) {
  let numerator = Math.pow(A, S) / factorial(S);
  let denominator = 0;
  for (let k = 0; k <= S; k++) {
    denominator += Math.pow(A, k) / factorial(k);
  }
  return numerator / denominator;
}

function factorial(n) {
  return n <= 1 ? 1 : n * factorial(n - 1);
}
