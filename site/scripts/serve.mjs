#!/usr/bin/env node
// 本機預覽 public/：只綁 127.0.0.1，套用 public/_headers 的 "/*" 規則，行為接近 Cloudflare assets-only。
//   node scripts/serve.mjs [--port 8788]   （或 PORT=8788）

import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', 'public');
const portFlag = process.argv.indexOf('--port');
const PORT = Number(portFlag > -1 ? process.argv[portFlag + 1] : process.env.PORT ?? 8788);
const HIDDEN = new Set(['/_headers', '/_redirects']);
const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.txt': 'text/plain; charset=utf-8',
  '.json': 'application/json',
};

async function globalHeaders() {
  const headers = {};
  let text;
  try {
    text = await readFile(path.join(ROOT, '_headers'), 'utf8');
  } catch {
    return headers;
  }
  let inGlobal = false;
  for (const line of text.split('\n')) {
    if (!line.trim() || line.trimStart().startsWith('#')) continue;
    if (!/^\s/.test(line)) { inGlobal = line.trim() === '/*'; continue; }
    const at = line.indexOf(':');
    if (inGlobal && at > 0) headers[line.slice(0, at).trim()] = line.slice(at + 1).trim();
  }
  return headers;
}

async function resolveFile(urlPath) {
  const decoded = decodeURIComponent(urlPath);
  if (HIDDEN.has(decoded)) return null;
  const candidate = path.resolve(ROOT, `.${decoded.endsWith('/') ? `${decoded}index.html` : decoded}`);
  if (candidate !== ROOT && !candidate.startsWith(`${ROOT}${path.sep}`)) return null;
  for (const file of [candidate, `${candidate}.html`]) {
    try {
      if ((await stat(file)).isFile()) return file;
    } catch { /* 試下一個 */ }
  }
  return null;
}

try {
  await stat(path.join(ROOT, 'index.html'));
} catch {
  console.error('public/index.html 不存在：請先執行 npm run build');
  process.exit(1);
}

const headers = await globalHeaders();
createServer(async (req, res) => {
  try {
    const { pathname } = new URL(req.url, 'http://localhost');
    const file = await resolveFile(pathname);
    const status = file ? 200 : 404;
    const served = file ?? path.join(ROOT, '404.html');
    const body = await readFile(served);
    res.writeHead(status, { ...headers, 'Content-Type': TYPES[path.extname(served)] ?? 'application/octet-stream', 'Cache-Control': 'no-store' });
    res.end(req.method === 'HEAD' ? undefined : body);
  } catch {
    res.writeHead(400, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('bad request');
  }
}).listen(PORT, '127.0.0.1', () => {
  console.log(`preview: http://127.0.0.1:${PORT}/  (Ctrl+C 結束)`);
});
