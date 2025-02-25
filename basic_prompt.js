function toCamelCase(str) {
    return str
        .toLowerCase()
        .replace(/[^a-zA-Z0-9]+(.)/g, (_, chr) => chr.toUpperCase());
}

// Examples:
// toCamelCase('user_id') => 'userId'
// toCamelCase('first-name') => 'firstName'
// toCamelCase('Some text') => 'someText'