const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Path to the backend urls.py file
const urlsFilePath = path.resolve(__dirname, '../../example_project_backend/example_project_backend/urls.py');
// Path to the api-config.service.ts file
const apiConfigFilePath = path.resolve(__dirname, '../src/app/shared/api/api-config.service.ts');

// Read the urls.py file
const urlsFileContent = fs.readFileSync(urlsFilePath, 'utf8');

// Extract paths from the urls.py file
// We're looking for lines like: path(r'auth/', auth_api.urls),
const pathRegex = /path\(r'([^']+)'/g;
const paths: string[] = [];
let match;

while ((match = pathRegex.exec(urlsFileContent)) !== null) {
  const pathUrl = match[1];
  // Skip admin paths
  if (!pathUrl.startsWith('admin')) {
    paths.push(pathUrl);
  }
}

console.log('Found paths:', paths);

// Create the generated-files directory if it doesn't exist
const generatedFilesDir = path.resolve(__dirname, '../src/generated-files');
if (!fs.existsSync(generatedFilesDir)) {
  fs.mkdirSync(generatedFilesDir, { recursive: true });
}

// Generate OpenAPI clients for each path
paths.forEach(pathUrl => {
  const outputDir = path.join(generatedFilesDir, pathUrl);

  // Create the output directory if it doesn't exist
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Run the OpenAPI command
  const command = `npx @hey-api/openapi-ts -i http://localhost:8000/${pathUrl}openapi.json -o src/generated-files/${pathUrl} -c @hey-api/client-fetch`;

  console.log(`Generating client for ${pathUrl}...`);
  console.log(`Running command: ${command}`);

  try {
    execSync(command, { stdio: 'inherit' });
    console.log(`Successfully generated client for ${pathUrl}`);
  } catch (error) {
    console.error(`Error generating client for ${pathUrl}:`, error);
  }
});

// Update the api-config.service.ts file
console.log('Updating api-config.service.ts...');

// Read the current content of the file
const apiConfigContent = fs.readFileSync(apiConfigFilePath, 'utf8');

// Generate import statements
const imports = paths.map(pathUrl => {
  // Convert path to a valid import path
  // For example: 'auth/' -> 'auth', 'api/users/' -> 'api/users'
  const importPath = pathUrl.endsWith('/') ? pathUrl.slice(0, -1) : pathUrl;
  // Convert path to a valid variable name
  // For example: 'auth/' -> 'authClient', 'api/users/' -> 'apiUsersClient'
  const clientName = importPath
    .replace(/\//g, '_') // Replace slashes with underscores
    .replace(/[^a-zA-Z0-9_]/g, '') // Remove any non-alphanumeric characters
    .replace(/^_+|_+$/g, '') // Remove leading/trailing underscores
    .replace(/_+/g, '_') // Replace multiple underscores with a single one
    + 'Client';

  return {
    importStatement: `import {client as ${clientName}} from '../../../generated-files/${importPath}/client.gen';`,
    clientName
  };
});

// Generate the new content
let newContent = '';

// Add imports
const importSection = imports.map(imp => imp.importStatement).join('\n');

// Replace the import section
newContent = apiConfigContent.replace(
  /import { Injectable } from '@angular\/core';[\s\S]*?(?=@Injectable)/,
  `import { Injectable } from '@angular/core';\n${importSection}\n\n`
);

// Replace the clients array
const clientsArray = `readonly clients = [${imports.map(imp => imp.clientName).join(', ')}];`;
newContent = newContent.replace(
  /readonly clients = \[[^\]]*\];/,
  clientsArray
);

// Write the updated content back to the file
fs.writeFileSync(apiConfigFilePath, newContent);

console.log('api-config.service.ts updated successfully');
console.log('Done!');
