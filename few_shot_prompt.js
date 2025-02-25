function toCamelCase(str) {
    if (!str) return '';
    
    // Split the string by spaces, underscores, or hyphens
    const words = str.split(/[\s_-]/g);
    
    // Convert first word to lowercase
    const firstWord = words[0].toLowerCase();
    
    // Convert remaining words to capitalize first letter and lowercase rest
    const restWords = words.slice(1).map(word => 
        word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    );
    
    // Join all words together
    return firstWord + restWords.join('');
}

// Test cases
console.log(toCamelCase('first name'));     // firstName
console.log(toCamelCase('user_id'));        // userId
console.log(toCamelCase('SCREEN_NAME'));    // screenName
console.log(toCamelCase('mobile-number'));  // mobileNumber