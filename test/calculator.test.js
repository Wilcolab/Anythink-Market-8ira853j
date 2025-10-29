const { add, multiply, divide } = require('../src/calculator');

describe('Math functions', () => {
  console.log('Running tests...');

  test('add function should correctly add two numbers', () => {
    const result = add(2, 3);
    expect(result).toBe(5);
    console.log('✅ Add test passed');
  });

  test('multiply function should correctly multiply two numbers', () => {
    const result = multiply(4, 5);
    expect(result).toBe(20);
    console.log('✅ Multiply test passed');
  });

  test('divide function should correctly divide two numbers', () => {
    const result = divide(10, 2);
    expect(result).toBe(5);
    console.log('✅ Divide test passed');
  });
});
