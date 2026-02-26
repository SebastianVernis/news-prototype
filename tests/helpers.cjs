const fs = require('fs');
const path = require('path');

function repoRoot() {
  return process.cwd();
}

function resolvePath(...parts) {
  return path.join(repoRoot(), ...parts);
}

function exists(relPath) {
  return fs.existsSync(resolvePath(relPath));
}

function read(relPath) {
  return fs.readFileSync(resolvePath(relPath), 'utf8');
}

function list(relPath) {
  return fs.readdirSync(resolvePath(relPath));
}

function isDirectory(relPath) {
  return fs.statSync(resolvePath(relPath)).isDirectory();
}

module.exports = {
  repoRoot,
  resolvePath,
  exists,
  read,
  list,
  isDirectory,
};
