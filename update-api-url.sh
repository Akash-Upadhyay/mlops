#!/bin/sh
# Update the API URL in JavaScript files

# Find all JavaScript files
find /usr/share/nginx/html -name "*.js" -type f -exec sed -i 's|http://localhost:30800|http://catvsdogclasifier.com/backend|g' {} \;

echo "API URL updated in JavaScript files" 