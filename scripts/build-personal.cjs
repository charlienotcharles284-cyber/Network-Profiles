const fs = require('node:fs');
const source = fs.readFileSync('JS/Runestone_V3.js', 'utf8');
const marker = /const RUNESTONE = \{repository: "[^"]+", personal: false\};/;
const output = source.replace(marker, 'const RUNESTONE = {repository: "charlienotcharles284-cyber/Network-Profiles", personal: true};');
const beta = source
 .replace('/* Runestone V3', '/* Runestone Charlie Beta (MIPS) — based on Runestone V3')
 .replace(marker, 'const RUNESTONE = {repository: "charlienotcharles284-cyber/Network-Profiles", personal: true, tunStack: "mips"};')
 .replace(
  '  const fixed = Object.assign({}, config);',
  '  const fixed = Object.assign({}, config);\n' +
  '  // Beta channel: change only the TUN stack; retain every other Hako network setting.\n' +
  '  fixed.tun = Object.assign({}, config.tun, {stack: RUNESTONE.tunStack});'
 );
if (output === source || beta === source || !beta.includes('stack: RUNESTONE.tunStack')) {
 throw new Error('Runestone build marker missing');
}
if (process.argv.includes('--check')) {
 if (fs.readFileSync('JS/Runestone_Charlie.js','utf8') !== output) throw new Error('Personal script is stale: node scripts/build-personal.cjs');
 if (fs.readFileSync('JS/Runestone_Charlie_Beta.js','utf8') !== beta) throw new Error('Beta script is stale: node scripts/build-personal.cjs');
} else {
 fs.writeFileSync('JS/Runestone_Charlie.js', output);
 fs.writeFileSync('JS/Runestone_Charlie_Beta.js', beta);
}
