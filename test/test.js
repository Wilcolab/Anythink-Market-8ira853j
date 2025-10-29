const calculator = require('../src/calculator');

console.log('Running tests...');

// Test add function
const addResult = calculator.add(2, 3);
if (addResult === 5) {
  console.log('✅ Add test passed');
} else {
  console.log('❌ Add test failed');
  process.exit(1);
}

// Test multiply function
const multiplyResult = calculator.multiply(4, 5);
if (multiplyResult === 20) {
  console.log('✅ Multiply test passed');
} else {
  console.log('❌ Multiply test failed');
  process.exit(1);
}

// Test divide function
const divideResult = calculator.divide(10, 2);
if (divideResult === 5) {
  console.log('✅ Divide test passed');
} else {
  console.log('❌ Divide test failed');
  process.exit(1);
}

console.log('All tests passed! 🎉');