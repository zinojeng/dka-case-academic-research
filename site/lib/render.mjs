// 由 clinical.json 產生完整靜態 HTML：主要教學文字不依賴 JavaScript 也能閱讀。
// 所有內容字串都經過 esc()；只有 [S02] 形式的引用會轉成站內錨點。

import { FIELDS, computeInfusion, formatInfusion } from '../src/assets/calc.js';
import { TOPIC_IDS } from './validate.mjs';

export const TAGLINE = '血糖下降後，還有哪些判斷不能省略';

// 計算機預填值：本例藥囑的算術例子。build 會確認 clinical.json 仍提到同一體重。
export const CALC_DEFAULTS = { units: '50', volumeMl: '500', rateLowMlH: '20', rateHighMlH: '30', weightKg: '104.5' };

const STATUS_LABEL = { known: '已知', caution: '需注意', unknown: '待核對' };
const EVIDENCE_LABEL = { order: '有醫囑', 'user-confirmed': '使用者確認', recorded: '紀錄可見' };

export function esc(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

// 內文的來源代號（[S02] 或 S02 §4）轉成文獻錨點；validate 已確保代號都存在。
// renderPage 是同步的，所以每次呼叫前設定一次即可。
let knownRefs = new Set();
const rich = (text) => esc(text)
  .replace(/\[(S\d{2,3})\]/g, (m, id) => (knownRefs.has(id) ? `<a class="cite" href="#ref-${id}">${id}</a>` : m))
  .replace(/(^|[^\w>#-])(S\d{2,3})(?![\w<])/g, (m, pre, id) => (knownRefs.has(id) ? `${pre}<a class="ref-link" href="#ref-${id}">${id}</a>` : m));
// 公開頁只顯示年月：content.updated 仍是 YYYY-MM-DD，但 HTML 內不出現完整日期。
const reviewMonth = (data) => `<time datetime="${esc(data.updated.slice(0, 7))}">${esc(data.updated.slice(0, 7))}</time>`;
const formatMl = (n) => `${n.toLocaleString('en-US')} mL`;
const signedMl = (n) => `${n > 0 ? '+' : n < 0 ? '−' : ''}${Math.abs(n).toLocaleString('en-US')} mL`;

function sectionHead(id, title, kicker = '') {
  return `<header class="section-head">
  ${kicker ? `<p class="kicker">${esc(kicker)}</p>` : ''}
  <h2>${esc(title)}</h2>
  <p class="section-tools"><a class="anchor" href="#${id}">本節連結</a><button class="copy-link" type="button" data-target="${id}" hidden>複製連結</button></p>
</header>`;
}

function paragraphs(list, idPrefix, className = '') {
  const cls = className ? ` class="${className}"` : '';
  return list.map((p, i) => `<p id="${idPrefix}-${i + 1}"${cls}>${rich(p)}</p>`).join('\n');
}

function sourceLine(ids, refsById) {
  const links = ids.map((id) => `<li><a href="#ref-${id}">${esc(id)}</a> ${esc(refsById.get(id).title)}</li>`).join('');
  return `<div class="sources"><p class="sources-label">來源</p><ul>${links}</ul></div>`;
}

function renderOverview(data) {
  const rows = data.metrics.map((m, i) => `<tr id="metric-${i + 1}" class="status-${m.status}">
  <th scope="row">${esc(m.label)}</th>
  <td data-label="數值"><span class="value">${esc(m.value)}</span>${m.unit ? ` <span class="unit">${esc(m.unit)}</span>` : ''}</td>
  <td data-label="狀態"><span class="badge badge-${m.status}">${STATUS_LABEL[m.status]}</span></td>
  <td data-label="說明">${m.note ? rich(m.note) : ''}</td>
</tr>`).join('\n');
  return `<section id="overview" class="section" data-search-title="概覽">
${sectionHead('overview', '先看全貌', '概覽')}
${paragraphs(data.overview, 'overview')}
<h3 id="metrics">關鍵數字</h3>
<div class="table-wrap">
<table class="metrics">
  <caption class="visually-hidden">關鍵數字與資料狀態</caption>
  <thead><tr><th scope="col">項目</th><th scope="col">數值</th><th scope="col">狀態</th><th scope="col">說明</th></tr></thead>
  <tbody>
${rows}
  </tbody>
</table>
</div>
<p class="legend"><span class="badge badge-known">已知</span> 紀錄可直接支持 <span class="badge badge-caution">需注意</span> 有值但解讀受限 <span class="badge badge-unknown">待核對</span> 紀錄中沒有，不能補造</p>
</section>`;
}

function renderTimeline(data) {
  const days = data.timeline.map((d, i) => `<li id="timeline-${i + 1}" class="day">
  <p class="day-label">${esc(d.day)}</p>
  <div class="day-body">
    <h3>${esc(d.title)}</h3>
    <ul>${d.items.map((item) => `<li>${rich(item)}</li>`).join('')}</ul>
  </div>
</li>`).join('\n');
  return `<section id="timeline" class="section" data-search-title="時間軸">
${sectionHead('timeline', 'Day 0–2 時間軸', '病程')}
<ol class="timeline">
${days}
</ol>
</section>`;
}

function renderKnown(data) {
  const list = (items, prefix) => items.map((x, i) => `<li id="${prefix}-${i + 1}">${rich(x)}</li>`).join('');
  return `<section id="known" class="section" data-search-title="已知／待核對">
${sectionHead('known', '已知與仍待核對', '判讀界線')}
<div class="split">
  <div class="split-col known-col">
    <h3>已知（可據以判讀）</h3>
    <ul class="check-list">${list(data.known, 'known')}</ul>
  </div>
  <div class="split-col unknown-col">
    <h3>仍待核對（不能補造）</h3>
    <ul class="check-list">${list(data.unknown, 'unknown')}</ul>
  </div>
</div>
</section>`;
}

function orderedTopics(data) {
  return TOPIC_IDS.map((id) => data.topics.find((t) => t.id === id));
}

function renderTopics(data, refsById) {
  const topics = orderedTopics(data);
  const nav = topics.map((t, i) => `<li><a href="#topic-${t.id}"><span class="num">${i + 1}</span><span class="nav-title">${esc(t.title)}</span></a><p>${rich(t.summary)}</p></li>`).join('\n');
  const sections = topics.map((t, i) => {
    const id = `topic-${t.id}`;
    return `<section id="${id}" class="section topic" data-search-title="第 ${i + 1} 題：${esc(t.title)}">
${sectionHead(id, t.title, `第 ${i + 1} 題`)}
<p id="${id}-summary" class="summary">${rich(t.summary)}</p>
${paragraphs(t.body, id)}
<details class="fellow" id="${id}-fellow">
  <summary>Fellow 深讀</summary>
  <div class="fellow-body">
${paragraphs(t.fellow, `${id}-fellow`)}
  </div>
</details>
<aside class="takeaway" aria-label="床邊重點"><p class="takeaway-label">床邊重點</p><p id="${id}-takeaway">${rich(t.takeaway)}</p></aside>
${sourceLine(t.sourceIds, refsById)}
</section>`;
  }).join('\n');
  return `<div id="topics" class="topics-group">
<section class="section topics-intro" aria-labelledby="topics-heading">
  <header class="section-head"><p class="kicker">五題</p><h2 id="topics-heading">五個不能省略的判斷</h2>
  <p class="section-tools"><a class="anchor" href="#topics">本節連結</a><button class="copy-link" type="button" data-target="topics" hidden>複製連結</button></p></header>
  <ol class="topic-nav">
${nav}
  </ol>
</section>
${sections}
</div>`;
}

function renderMedications(data) {
  const rows = data.medications.map((m, i) => `<tr id="med-${i + 1}">
  <th scope="row">${esc(m.name)}</th>
  <td data-label="醫囑內容">${rich(m.order)}</td>
  <td data-label="證據"><span class="badge badge-ev-${m.evidence}">${EVIDENCE_LABEL[m.evidence]}</span></td>
  <td data-label="教學重點">${rich(m.teaching)}</td>
</tr>`).join('\n');
  return `<section id="medications" class="section" data-search-title="相關藥囑辨識">
${sectionHead('medications', '相關藥囑辨識', '藥囑')}
<p class="note">「有醫囑」表示有開立紀錄，不等於已經給完；實際給了多少要核對給藥紀錄（MAR）。</p>
<div class="table-wrap">
<table class="meds">
  <caption class="visually-hidden">與 DKA 教學相關的藥囑</caption>
  <thead><tr><th scope="col">藥品</th><th scope="col">醫囑內容</th><th scope="col">證據</th><th scope="col">教學重點</th></tr></thead>
  <tbody>
${rows}
  </tbody>
</table>
</div>
</section>`;
}

function renderCalculator() {
  const example = computeInfusion(CALC_DEFAULTS);
  if (!example.ok) throw new Error(`計算機預設值無法計算：${JSON.stringify(example.errors)}`);
  const f = formatInfusion(example);
  const outputs = [
    ['concentration', '濃度', f.concentration],
    ['unitsPerHour', '每小時 insulin', f.unitsPerHour],
    ['unitsPerKgHour', '換算體重', f.unitsPerKgHour],
    ['bagHours', '整袋輸完需時', f.bagHours],
    ['vehicleMlPerDay', '每日 vehicle 液量', f.vehicleMlPerDay],
  ];
  const dl = outputs.map(([key, label, value]) => `<div><dt>${label}</dt><dd data-out="${key}">${esc(value)}</dd></div>`).join('');
  const fields = Object.entries(FIELDS).map(([key, spec]) => `<div class="field">
    <label for="calc-${key}">${esc(spec.label)} <span class="unit">${esc(spec.unit)}</span></label>
    <input id="calc-${key}" name="${key}" type="text" inputmode="decimal" autocomplete="off" spellcheck="false" value="${esc(CALC_DEFAULTS[key])}" aria-describedby="calc-${key}-error"${spec.optional ? '' : ' required'}>
    <p class="field-error" id="calc-${key}-error" hidden></p>
  </div>`).join('\n');
  return `<section id="calculator" class="section" data-search-title="Insulin 稀釋算術校驗">
${sectionHead('calculator', 'Insulin 稀釋算術校驗', '算術')}
<p id="calculator-1">只做單位換算：濃度 = 總單位 ÷ 總體積；每小時 insulin = 速率 × 濃度；每公斤每小時 = 每小時 insulin ÷ 體重；整袋需時 = 體積 ÷ 速率。</p>
<aside class="warning" role="note">
  <p><strong>這不是劑量建議。</strong>算出的數字不代表應該調高或調低速率。鉀（K）與最新 BOHB 尚未確認前，不能只依算術調整 insulin dose；實際產品、配製與 hang time 需和藥局及院內流程核對。</p>
</aside>
<h3 id="calc-example-heading">本例算術（50 U / 500 mL；20 / 30 mL/h；104.5 kg）</h3>
<dl class="calc-output calc-example" aria-labelledby="calc-example-heading">${dl}</dl>
<noscript><p class="note">互動計算需要 JavaScript；上方為本例數值的預先計算結果。</p></noscript>
<form id="calc-form" class="calc" novalidate hidden aria-labelledby="calc-form-heading">
  <h3 id="calc-form-heading">自行輸入核對</h3>
  <p class="note">所有計算在你的瀏覽器本機完成，不會送出或儲存。</p>
  <div class="fields">
${fields}
  </div>
  <p class="form-error" id="calc-form-error" role="alert" hidden></p>
  <div class="actions"><button type="submit">計算</button><button type="reset" class="secondary">還原本例數值</button></div>
  <div class="calc-live" role="status" aria-live="polite">
    <dl class="calc-output" id="calc-result">${dl}</dl>
    <p class="calc-flag" id="calc-flag" hidden></p>
  </div>
</form>
</section>`;
}

function renderIo(data) {
  const io = data.io;
  return `<section id="io" class="section" data-search-title="I/O 部分紀錄">
${sectionHead('io', 'I/O 部分紀錄', '出入量')}
<p id="io-label" class="summary">${rich(io.label)}</p>
<dl class="io-figures">
  <div><dt>輸入</dt><dd>${formatMl(io.inputMl)}</dd></div>
  <div><dt>尿量</dt><dd>${formatMl(io.urineMl)}</dd></div>
  <div><dt>差值（輸入 − 尿量）</dt><dd>${signedMl(io.differenceMl)}</dd></div>
</dl>
<h3>解讀限制</h3>
<ul class="check-list">${io.caveats.map((c, i) => `<li id="io-caveat-${i + 1}">${rich(c)}</li>`).join('')}</ul>
</section>`;
}

const LETTERS = 'ABCDEFGHIJ';

function renderQuiz(data, refsById) {
  const items = data.quizzes.map((q, i) => {
    const name = `q-${q.id}`;
    const options = q.options.map((opt, j) => `<li><label class="option"><input type="radio" name="${name}" value="${j}"><span class="letter">${LETTERS[j] ?? j + 1}</span><span class="option-text">${rich(opt)}</span></label></li>`).join('');
    return `<div class="quiz-item" id="quiz-${q.id}" data-quiz-id="${esc(q.id)}" data-answer="${q.answer}">
  <fieldset>
    <legend><span class="q-num">第 ${i + 1} 題</span>${rich(q.question)}</legend>
    <ul class="options">${options}</ul>
  </fieldset>
  <p class="quiz-feedback" hidden></p>
  <details class="quiz-answer">
    <summary>看答案與解析</summary>
    <p class="answer-line"><strong>正確答案：</strong>${LETTERS[q.answer] ?? q.answer + 1}. ${rich(q.options[q.answer])}</p>
    <p>${rich(q.explanation)}</p>
    ${sourceLine(q.sourceIds, refsById)}
  </details>
</div>`;
  }).join('\n');
  return `<section id="quiz" class="section" data-search-title="自我測驗">
${sectionHead('quiz', '自我測驗', '測驗')}
<p id="quiz-1">每題選一個答案，會立即看到解析與來源。作答紀錄只存在這台裝置的瀏覽器。</p>
<div class="quiz-bar" hidden><p class="quiz-progress" id="quiz-progress" role="status">已作答 0 / ${data.quizzes.length}</p><button type="button" class="secondary" id="quiz-reset">重設測驗</button></div>
${items}
</section>`;
}

function renderReferences(data) {
  const items = data.references.map((r) => `<li id="ref-${esc(r.id)}"><span class="ref-id">${esc(r.id)}</span> <a href="${esc(r.url)}" rel="noopener noreferrer" target="_blank">${esc(r.title)}</a></li>`).join('\n');
  return `<section id="references" class="section" data-search-title="參考文獻">
${sectionHead('references', '參考文獻', '來源')}
<p class="note">文獻查核月份：${reviewMonth(data)}。</p>
<ol class="refs">
${items}
</ol>
</section>`;
}

function renderToc(data) {
  const topics = orderedTopics(data).map((t, i) => `<li><a href="#topic-${t.id}"><span class="num">${i + 1}</span>${esc(t.title)}</a></li>`).join('');
  return `<nav class="toc" aria-label="章節導航">
<details class="toc-details" open>
  <summary>章節目錄</summary>
  <div class="search" hidden>
    <label for="site-search">搜尋本頁</label>
    <input id="site-search" type="search" autocomplete="off" placeholder="例如 phosphate、K、overlap" aria-describedby="search-status">
    <p id="search-status" class="search-status" role="status"></p>
    <ul id="search-results" class="search-results"></ul>
  </div>
  <ol class="toc-list">
    <li><a href="#overview">概覽與關鍵數字</a></li>
    <li><a href="#timeline">Day 0–2 時間軸</a></li>
    <li><a href="#known">已知／待核對</a></li>
    <li><a href="#topics">五題</a><ol class="toc-topics">${topics}</ol></li>
    <li><a href="#medications">相關藥囑辨識</a></li>
    <li><a href="#calculator">Insulin 稀釋算術</a></li>
    <li><a href="#io">I/O 部分紀錄</a></li>
    <li><a href="#quiz">自我測驗</a></li>
    <li><a href="#references">參考文獻</a></li>
  </ol>
</details>
</nav>`;
}

function head(title, description) {
  return `<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(description)}">
<meta name="robots" content="noindex">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/styles.css">`;
}

export function renderPage(data) {
  const refsById = new Map(data.references.map((r) => [r.id, r]));
  knownRefs = new Set(refsById.keys());
  return `${head(`${data.title}｜${TAGLINE}`, `${data.title}：${TAGLINE}。${data.audience} 教學用去識別個案。`)}
<script type="module" src="/assets/app.js"></script>
</head>
<body data-mode="pgy">
<a class="skip-link" href="#main">跳到主要內容</a>
<header class="masthead">
  <div class="masthead-inner">
    <p class="eyebrow">${esc(data.audience)} 教學個案 · 已去識別</p>
    <h1>${esc(data.title)}</h1>
    <p class="tagline">${TAGLINE}</p>
    <p class="meta">文獻查核月份 ${reviewMonth(data)} · 教學討論用，不是個人化醫囑</p>
    <div class="mode-switch" role="group" aria-label="閱讀深度" hidden>
      <button type="button" data-mode="pgy" aria-pressed="true">PGY 重點</button>
      <button type="button" data-mode="fellow" aria-pressed="false">Fellow 深讀</button>
    </div>
  </div>
</header>
<div class="layout">
${renderToc(data)}
<main id="main" tabindex="-1">
${renderOverview(data)}
${renderTimeline(data)}
${renderKnown(data)}
${renderTopics(data, refsById)}
${renderMedications(data)}
${renderCalculator()}
${renderIo(data)}
${renderQuiz(data, refsById)}
${renderReferences(data)}
</main>
</div>
<footer class="site-footer">
  <p>本站為教學用途的去識別個案討論，不提供個人化處方或固定輸注速率；臨床處置請依主治團隊判斷與院內流程。</p>
  <p>不需帳號、不收集輸入、不使用 analytics；計算與測驗都在瀏覽器本機進行。</p>
  <p><a href="#main">回到頁首</a></p>
</footer>
</body>
</html>
`;
}

export function renderNotFound(data) {
  return `${head(`找不到頁面｜${data.title}`, `${data.title} 找不到頁面`)}
</head>
<body>
<main class="not-found">
  <h1>找不到這個頁面</h1>
  <p><a href="/">回到 ${esc(data.title)}</a></p>
</main>
</body>
</html>
`;
}
