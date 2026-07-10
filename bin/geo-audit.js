#!/usr/bin/env node
/**
 * geo-audit CLI — Run GEO audit from command line
 * Usage: npx geo-audit https://yoursite.com
 */
const { execSync } = require('child_process');
const url = process.argv[2];
if (!url) {
  console.log('Usage: npx geo-audit https://yoursite.com');
  process.exit(1);
}
try {
  execSync(`python3 ${__dirname}/../scripts/audit.py ${url}`, { stdio: 'inherit' });
} catch (e) {
  process.exit(1);
}
