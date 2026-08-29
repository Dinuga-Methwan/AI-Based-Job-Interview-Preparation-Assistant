const fs = require('fs');
const path = require('path');
const filePath = path.resolve(__dirname, 'src/pages/LandingPage.tsx');
const buf = fs.readFileSync(filePath);
const result = {
  first30Hex: buf.slice(0,30).toString('hex'),
  containsCRLF: buf.includes(Buffer.from('\r\n')),
  containsBOM: buf[0]===0xEF && buf[1]===0xBB && buf[2]===0xBF,
  length: buf.length,
  first100Utf8: buf.slice(0,100).toString('utf8')
};
console.log(JSON.stringify(result, null, 2));
