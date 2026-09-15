const fs = require('node:fs');
const source = fs.readFileSync('JS/Runestone_V3.js', 'utf8');
const output = source.replace(/const RUNESTONE = \{repository: "[^"]+", personal: false\};/, 'const RUNESTONE = {repository: "charlienotcharles284-cyber/Network-Profiles", personal: true};');
if (output === source) throw new Error('Runestone settings marker missing');
if (process.argv.includes('--check')) {
 if (fs.readFileSync('JS/Runestone_Charlie.js','utf8') !== output) throw new Error('Personal script is stale: node scripts/build-personal.cjs');
} else fs.writeFileSync('JS/Runestone_Charlie.js', output);
