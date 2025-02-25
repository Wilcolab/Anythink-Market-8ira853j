/**
 * Converts a string to camelCase format.
 * Handles multiple word separators (spaces, hyphens, underscores)
 * and accounts for various edge cases.
 *
 * @param {string} str - The input string to convert
 * @returns {string} The camelCase converted string
 * @throws {TypeError} If input is not a string
 *
 * @example
 * toCamelCase("hello world") // returns "helloWorld"
 * toCamelCase("hello-world") // returns "helloWorld"
 * toCamelCase("Hello_World") // returns "helloWorld"
 */
function toCamelCase(str) {
    // Type checking
    if (typeof str !== 'string') {
        throw new TypeError('Input must be a string');
    }

    // Handle empty or whitespace-only strings
    if (!str.trim()) {
        return '';
    }

    return str
        // Replace special characters with spaces
        .replace(/[^a-zA-Z0-9\s_-]/g, '')
        // Split on any combination of spaces, underscores, or hyphens
        .split(/[\s_-]+/)
        // Map through words
        .map((word, index) => {
            // Convert word to lowercase
            word = word.toLowerCase();
            // Capitalize first letter of each word except the first one
            return index === 0 ? word : word.charAt(0).toUpperCase() + word.slice(1);
        })
        // Join words back together
        .join('');
}


/**
 * Converts a string to dot.case format.
 * Handles multiple word separators (spaces, hyphens, underscores)
 * and converts to lowercase words separated by dots.
 *
 * @param {string} str - The input string to convert
 * @returns {string} The dot.case converted string
 * @throws {TypeError} If input is not a string
 *
 * @example
 * toDotCase("hello world") // returns "hello.world"
 * toDotCase("helloWorld") // returns "hello.world"
 * toDotCase("Hello-World") // returns "hello.world"
 */
function toDotCase(str) {
    if (typeof str !== 'string') {
        throw new TypeError('Input must be a string');
    }

    if (!str.trim()) {
        return '';
    }

    return str
        .replace(/[^a-zA-Z0-9\s_-]/g, '')
        .replace(/([a-z])([A-Z])/g, '$1 $2')
        .split(/[\s_-]+/)
        .map(word => word.toLowerCase())
        .join('.');
}