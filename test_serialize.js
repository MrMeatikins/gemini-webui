const { Terminal } = require('xterm');
const { SerializeAddon } = require('xterm-addon-serialize');
const term = new Terminal();
const serializeAddon = new SerializeAddon();
term.loadAddon(serializeAddon);
term.write('\x1b[31mRed \x1b[32mGreen\x1b[0m');
console.log(serializeAddon.serializeAsHTML());
