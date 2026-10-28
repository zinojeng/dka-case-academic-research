#!/usr/bin/env node
// 讀 content/clinical.json → 驗證 → 產生 public/。任何問題都以非零 exit code 結束；舊 public/ 會先備份，替換失敗時還原。
//   node build.mjs [--content path/to/clinical.json] [--out path/to/public]

import { existsSync } from 'node:fs';
import { cp, mkdir, readFile, rename, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { CALC_DEFAULTS, esc, renderNotFound, renderPage } from './lib/render.mjs';
import { findFullDates, scanText, validateContent } from './lib/validate.mjs';

const SITE_DIR = path.dirname(fileURLToPath(import.meta.url));

export class BuildError extends Error {
  constructor(message, problems = []) {
    super(problems.length ? `${message}\n${problems.map((p) => `  - ${p}`).join('\n')}` : message);
    this.problems = problems;
  }
}

export async function loadContent(contentPath) {
  let raw;
  try {
    raw = await readFile(contentPath, 'utf8');
  } catch (err) {
    if (err.code === 'ENOENT') throw new BuildError(`找不到 ${contentPath}：臨床內容尚未交付，拒絕產生網站。`);
    throw err;
  }
  try {
    return JSON.parse(raw);
  } catch (err) {
    throw new BuildError(`${contentPath} 不是有效 JSON：${err.message}`);
  }
}

// 產出的 HTML 再掃一次可見文字，確保模板本身也沒有把私密字串帶進 public/。
// 文獻標題（含 article number 這類長數字）已在 JSON 檢查過，這裡先移除再掃長數字。
// 完整日期（YYYY-MM-DD 等）在 HTML 任何位置都不允許，包括 datetime 等屬性；只略過外部 href。
export function scanOutput(file, html, data) {
  const visible = html.replace(/<[^>]*>/g, ' ');
  const withoutRefs = data.references.reduce((text, ref) => text.replaceAll(esc(ref.title), ' '), visible);
  const dates = findFullDates(html.replace(/\shref="[^"]*"/g, '')).map((d) => `完整日期 "${d}"（公開頁只可顯示年月）`);
  return [...new Set([
    ...scanText(visible, { allowLongNumbers: true }),
    ...scanText(withoutRefs),
    ...dates,
  ])].map((p) => `public/${file}: ${p}`);
}

// renameDir 只供測試注入失敗情境；正常使用 fs.rename。
export async function build({ contentPath = path.join(SITE_DIR, 'content', 'clinical.json'), outDir = path.join(SITE_DIR, 'public'), renameDir = rename } = {}) {
  const data = await loadContent(contentPath);
  const { errors } = validateContent(data);
  if (errors.length) throw new BuildError(`clinical.json 未通過檢查（${errors.length} 項）`, errors);

  const flattened = JSON.stringify(data);
  if (!flattened.includes(CALC_DEFAULTS.weightKg)) {
    throw new BuildError(`計算機預設體重 ${CALC_DEFAULTS.weightKg} kg 未出現在 clinical.json；請確認體重是否更新，並同步 lib/render.mjs 的 CALC_DEFAULTS。`);
  }

  const html = renderPage(data);
  const notFound = renderNotFound(data);
  const outputProblems = [...scanOutput('index.html', html, data), ...scanOutput('404.html', notFound, data)];
  if (outputProblems.length) throw new BuildError('產出的 HTML 含有不可公開的內容', outputProblems);

  // 先寫到暫存目錄；替換時把舊 public/ 改名為備份，新目錄就位後才刪備份。
  // rename 失敗時把備份改回來，所以舊 build 不會因替換失敗而消失（但兩次 rename 之間仍有極短空窗）。
  const stamp = `${process.pid}-${Date.now()}`;
  const tmpDir = `${outDir}.tmp-${stamp}`;
  const backupDir = `${outDir}.bak-${stamp}`;
  await rm(tmpDir, { recursive: true, force: true });
  await mkdir(tmpDir, { recursive: true });
  let backedUp = false;
  try {
    await cp(path.join(SITE_DIR, 'src', 'assets'), path.join(tmpDir, 'assets'), { recursive: true });
    await cp(path.join(SITE_DIR, 'src', 'static'), tmpDir, { recursive: true });
    await writeFile(path.join(tmpDir, 'index.html'), html);
    await writeFile(path.join(tmpDir, '404.html'), notFound);
    if (existsSync(outDir)) {
      await renameDir(outDir, backupDir);
      backedUp = true;
    }
    await renameDir(tmpDir, outDir);
  } catch (err) {
    if (backedUp && !existsSync(outDir)) await renameDir(backupDir, outDir);
    await rm(tmpDir, { recursive: true, force: true });
    throw err;
  }
  if (backedUp) await rm(backupDir, { recursive: true, force: true });
  return { outDir, html, data };
}

function parseArgs(argv) {
  const opts = {};
  for (let i = 0; i < argv.length; i += 1) {
    const flag = argv[i];
    if (flag === '--content' || flag === '--out') {
      const value = argv[++i];
      if (!value) throw new BuildError(`${flag} 需要路徑`);
      opts[flag === '--content' ? 'contentPath' : 'outDir'] = path.resolve(value);
    } else {
      throw new BuildError(`未知參數 ${flag}`);
    }
  }
  return opts;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const { outDir, data } = await build(parseArgs(process.argv.slice(2)));
    console.log(`built ${path.relative(process.cwd(), outDir) || outDir}: ${data.topics.length} topics, ${data.quizzes.length} quizzes, ${data.references.length} references`);
  } catch (err) {
    console.error(err instanceof BuildError ? `build failed: ${err.message}` : err);
    process.exitCode = 1;
  }
}
