const { JSDOM } = require('jsdom');
const dom = new JSDOM('<!DOCTYPE html><div id="terminal"></div>');
global.window = dom.window;
global.document = dom.window.document;
global.navigator = dom.window.navigator;
const { Terminal } = require('xterm');
const { SerializeAddon } = require('xterm-addon-serialize');

const term = new Terminal();
const serializeAddon = new SerializeAddon();
term.loadAddon(serializeAddon);
term.open(document.getElementById('terminal'));
term.write('\x1b[31mRed \x1b[32mGreen\x1b[0m');
console.log("DEFAULT:");
console.log(serializeAddon.serializeAsHTML());
console.log("WITH GLOBAL BG:");
console.log(serializeAddon.serializeAsHTML({includeGlobalBackground: true}));
