import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { build, BuildError, scanOutput } from '../build.mjs';

const FIXTURE = fileURLToPath(new URL('./fixtures/clinical.fixture.json', import.meta.url));
const fixture = () => JSON.parse(readFileSync(FIXTURE, 'utf8'));

function workspace(t) {
  const dir = mkdtempSync(path.join(tmpdir(), 'dka-site-test-'));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  return dir;
}

function writeContent(dir, data) {
  const file = path.join(dir, 'clinical.json');
  writeFileSync(file, typeof data === 'string' ? data : JSON.stringify(data));
  return file;
}

const textOnly = (html) => html.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');

test('build 產生可部署的 public/ 結構', async (t) => {
  const dir = workspace(t);
  const outDir = path.join(dir, 'public');
  await build({ contentPath: FIXTURE, outDir });
  assert.deepEqual(readdirSync(outDir).sort(), ['.assetsignore', '404.html', '_headers', 'assets', 'index.html', 'robots.txt']);
  assert.deepEqual(readdirSync(path.join(outDir, 'assets')).sort(), ['app.js', 'calc.js', 'icon.svg', 'quiz.js', 'styles.css']);
  const headers = readFileSync(path.join(outDir, '_headers'), 'utf8');
  assert.match(headers, /Content-Security-Policy: default-src 'none'; script-src 'self'/);
  assert.match(headers, /connect-src 'none'/);
});

test('不用 JavaScript 也讀得到主要教學內容', async (t) => {
  const { html } = await build({ contentPath: FIXTURE, outDir: path.join(workspace(t), 'public') });
  const text = textOnly(html);
  const data = fixture();
  for (const p of [...data.overview, ...data.known, ...data.unknown, ...data.io.caveats]) {
    assert.ok(text.includes(p.replace(/\s*\[S\d+\]/g, '').trim().slice(0, 12)), `缺少：${p}`);
  }
  for (const topic of data.topics) {
    for (const s of [topic.title, topic.summary, ...topic.body, ...topic.fellow, topic.takeaway]) assert.ok(text.includes(s), `缺少 ${topic.id}: ${s}`);
  }
  for (const q of data.quizzes) assert.ok(text.includes(q.explanation), `缺少解析：${q.id}`);
  // 計算機的本例結果在 build 時算好
  assert.match(text, /0\.1 U\/mL/);
  assert.match(text, /2 \/ 3 U\/h/);
  assert.match(text, /0\.019 \/ 0\.029 U\/kg\/h/);
  assert.match(text, /25 \/ 16\.7 h/);
  assert.match(text, /\+896 mL/);
});

test('公開頁只顯示文獻查核月份，HTML 任何位置都沒有完整日期', async (t) => {
  const outDir = path.join(workspace(t), 'public');
  const { html } = await build({ contentPath: FIXTURE, outDir });
  assert.equal(fixture().updated, '2026-10-28', 'fixture 的 updated 仍是完整日期輸入');
  assert.equal(html.match(/文獻查核月份：?\s*<time datetime="2026-10">2026-10<\/time>/g)?.length, 2, '頁首與文獻區都標示查核月份');
  for (const file of ['index.html', '404.html']) {
    const raw = readFileSync(path.join(outDir, file), 'utf8');
    assert.deepEqual(raw.match(/\d{4}-\d{2}-\d{2}/g), null, `${file} 不應含 YYYY-MM-DD`);
    assert.ok(!raw.includes('2026/10/28') && !raw.includes('2026.10.28'));
  }
});

test('內文寫入完整日期（即使與 updated 相同）時 build 失敗', async (t) => {
  const data = fixture();
  data.references[0].title += ' Accessed 2026-10-28.';
  const dir = workspace(t);
  await assert.rejects(build({ contentPath: writeContent(dir, data), outDir: path.join(dir, 'public') }), /完整日期 "2026-10-28"/);
});

test('五題依固定順序排列，Fellow 深讀收在 details 中', async (t) => {
  const data = fixture();
  data.topics.reverse();
  const { html } = await build({ contentPath: writeContent(workspace(t), data), outDir: path.join(workspace(t), 'public') });
  const order = [...html.matchAll(/<section id="topic-([a-z-]+)"/g)].map((m) => m[1]);
  assert.deepEqual(order, ['calcium-phosphate', 'sodium', 'potassium', 'fluids', 'insulin']);
  assert.match(html, /<details class="fellow" id="topic-sodium-fellow">[\s\S]*?深讀段落 B。[\s\S]*?<\/details>/);
});

test('引用、測驗答案與文獻錨點彼此對得上', async (t) => {
  const { html } = await build({ contentPath: FIXTURE, outDir: path.join(workspace(t), 'public') });
  assert.match(html, /<a class="cite" href="#ref-S02">S02<\/a>/);
  const data = fixture();
  data.topics[1].fellow[0] = '依 S03 §16 與（S04）。';
  const { html: linked } = await build({ contentPath: writeContent(workspace(t), data), outDir: path.join(workspace(t), 'public') });
  assert.match(linked, /依 <a class="ref-link" href="#ref-S03">S03<\/a> §16 與（<a class="ref-link" href="#ref-S04">S04<\/a>）。/);
  const anchors = new Set([...html.matchAll(/ id="([^"]+)"/g)].map((m) => m[1]));
  for (const [, target] of html.matchAll(/href="#([^"]+)"/g)) assert.ok(anchors.has(target), `斷掉的站內連結 #${target}`);
  const answers = [...html.matchAll(/data-quiz-id="([^"]+)" data-answer="(\d+)"/g)].map((m) => [m[1], Number(m[2])]);
  assert.deepEqual(answers, fixture().quizzes.map((q) => [q.id, q.answer]));
});

test('內容中的 HTML 一律被跳脫', async (t) => {
  const data = fixture();
  data.overview.push('<script>alert(1)</script> & <img src=x onerror=alert(2)>');
  data.quizzes[0].options[0] = '"><b>bold</b>';
  const { html } = await build({ contentPath: writeContent(workspace(t), data), outDir: path.join(workspace(t), 'public') });
  assert.ok(!html.includes('<script>alert'));
  assert.ok(!html.includes('<img src=x'));
  assert.ok(!html.includes('<b>bold</b>'));
  assert.ok(html.includes('&lt;script&gt;alert(1)&lt;/script&gt; &amp; &lt;img'));
});

test('沒有 inline script / style，也沒有外部資源', async (t) => {
  const { html } = await build({ contentPath: FIXTURE, outDir: path.join(workspace(t), 'public') });
  for (const [tag] of html.matchAll(/<script\b[^>]*>/g)) assert.match(tag, /src="\/assets\//);
  assert.ok(!/<style\b|\sstyle="/.test(html));
  assert.ok(!/\son[a-z]+="/i.test(html), '不應有 inline event handler');
  for (const [, url] of html.matchAll(/(?:src|href)="(https?:[^"]+)"/g)) {
    assert.ok(fixture().references.some((r) => r.url === url), `非文獻的外部連結：${url}`);
  }
});

test('缺 clinical.json 時 build 失敗，且不產生 public/', async (t) => {
  const dir = workspace(t);
  const outDir = path.join(dir, 'public');
  await assert.rejects(build({ contentPath: path.join(dir, 'missing.json'), outDir }), (err) => err instanceof BuildError && /尚未交付/.test(err.message));
  assert.equal(existsSync(outDir), false);
});

test('無效內容讓 build 失敗，既有 public/ 保持不變', async (t) => {
  const dir = workspace(t);
  const outDir = path.join(dir, 'public');
  await build({ contentPath: FIXTURE, outDir });
  const before = readFileSync(path.join(outDir, 'index.html'), 'utf8');

  const broken = fixture();
  broken.topics[0].body[0] = 'TODO';
  await assert.rejects(build({ contentPath: writeContent(dir, broken), outDir }), /placeholder/);
  await assert.rejects(build({ contentPath: writeContent(dir, '{ not json'), outDir }), /不是有效 JSON/);
  assert.equal(readFileSync(path.join(outDir, 'index.html'), 'utf8'), before);
  assert.deepEqual(readdirSync(dir).filter((f) => f.includes('.tmp-')), []);
});

test('替換 public/ 失敗時還原舊 build，且不留下暫存或備份目錄', async (t) => {
  const dir = workspace(t);
  const outDir = path.join(dir, 'public');
  await build({ contentPath: FIXTURE, outDir });
  const before = readFileSync(path.join(outDir, 'index.html'), 'utf8');

  const data = fixture();
  data.overview[0] = '新版內容，不應出現在還原後的 public/。';
  const { rename } = await import('node:fs/promises');
  const failingRename = async (from, to) => {
    if (from.includes('.tmp-')) throw Object.assign(new Error('simulated rename failure'), { code: 'EXDEV' });
    return rename(from, to);
  };
  await assert.rejects(build({ contentPath: writeContent(dir, data), outDir, renameDir: failingRename }), /simulated rename failure/);
  assert.equal(readFileSync(path.join(outDir, 'index.html'), 'utf8'), before);
  assert.deepEqual(readdirSync(dir).filter((f) => /\.(tmp|bak)-/.test(f)), []);

  // 成功時也要清掉備份
  await build({ contentPath: writeContent(dir, data), outDir });
  assert.match(readFileSync(path.join(outDir, 'index.html'), 'utf8'), /新版內容/);
  assert.deepEqual(readdirSync(dir).filter((f) => /\.(tmp|bak)-/.test(f)), []);
});

test('scanOutput 依檔名標示問題，index.html 與 404.html 都會掃', async (t) => {
  const data = fixture();
  assert.deepEqual(scanOutput('404.html', '<p>找不到 TODO</p><time datetime="2026-10-28"></time>', data), [
    'public/404.html: placeholder 標記',
    'public/404.html: 完整日期 "2026-10-28"（公開頁只可顯示年月）',
  ]);
  assert.deepEqual(scanOutput('index.html', '<p>/Users/x</p>', data), ['public/index.html: 本機絕對路徑']);
  const outDir = path.join(workspace(t), 'public');
  const { html } = await build({ contentPath: FIXTURE, outDir });
  assert.deepEqual(scanOutput('index.html', html, data), []);
  assert.deepEqual(scanOutput('404.html', readFileSync(path.join(outDir, '404.html'), 'utf8'), data), []);
});

test('計算機預設體重與 clinical.json 不同步時 build 失敗', async (t) => {
  const data = JSON.parse(JSON.stringify(fixture()).replaceAll('104.5', '98'));
  const dir = workspace(t);
  await assert.rejects(build({ contentPath: writeContent(dir, data), outDir: path.join(dir, 'public') }), /預設體重 104\.5 kg/);
});
