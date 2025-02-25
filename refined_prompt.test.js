const { toCamelCase } = require('./refined_prompt');

describe('toCamelCase function', () => {
    test('converts space-separated words to camelCase', () => {
        expect(toCamelCase('hello world')).toBe('helloWorld');
        expect(toCamelCase('foo bar baz')).toBe('fooBarBaz');
    });

    test('converts hyphen-separated words to camelCase', () => {
        expect(toCamelCase('hello-world')).toBe('helloWorld');
        expect(toCamelCase('foo-bar-baz')).toBe('fooBarBaz');
    });

    test('converts underscore-separated words to camelCase', () => {
        expect(toCamelCase('hello_world')).toBe('helloWorld');
        expect(toCamelCase('foo_bar_baz')).toBe('fooBarBaz');
    });

    test('handles mixed separators correctly', () => {
        expect(toCamelCase('hello-world_foo bar')).toBe('helloWorldFooBar');
    });

    test('preserves first word in lowercase', () => {
        expect(toCamelCase('Hello World')).toBe('helloWorld');
        expect(toCamelCase('HELLO WORLD')).toBe('helloWorld');
    });

    test('handles empty strings', () => {
        expect(toCamelCase('')).toBe('');
        expect(toCamelCase('   ')).toBe('');
    });

    test('removes special characters', () => {
        expect(toCamelCase('hello@world')).toBe('helloWorld');
        expect(toCamelCase('hello#$%world')).toBe('helloWorld');
    });

    test('throws TypeError for non-string inputs', () => {
        expect(() => toCamelCase(123)).toThrow(TypeError);
        expect(() => toCamelCase(null)).toThrow(TypeError);
        expect(() => toCamelCase(undefined)).toThrow(TypeError);
        expect(() => toCamelCase({})).toThrow(TypeError);
    });
});