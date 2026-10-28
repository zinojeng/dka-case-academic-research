// 漸進增強：主要內容已在 HTML 中；這裡只加上閱讀模式、搜尋、複製連結、計算機與測驗。
// 所有動態文字一律用 textContent，不用 innerHTML。

import { FIELDS, computeInfusion, formatInfusion, LABEL_CONCENTRATION_U_PER_ML } from './calc.js';
import { gradeAnswer, restoreAnswers, summarize } from './quiz.js';

const MODE_KEY = 'dka-rounds:mode';
const QUIZ_KEY = 'dka-rounds:quiz-v1';
const narrowScreen = window.matchMedia('(max-width: 959px)');

const storage = {
  get(key) {
    try { return window.localStorage.getItem(key); } catch { return null; }
  },
  set(key, value) {
    try { window.localStorage.setItem(key, value); } catch { /* 私密模式或被封鎖時就只在本次頁面有效 */ }
  },
  remove(key) {
    try { window.localStorage.removeItem(key); } catch { /* 同上 */ }
  },
};

document.documentElement.classList.add('js');

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function openAncestors(node) {
  for (let d = node.closest('details'); d; d = d.parentElement?.closest('details')) d.open = true;
}

// ---- 閱讀模式 ---------------------------------------------------------------
function initMode() {
  const group = document.querySelector('.mode-switch');
  if (!group) return;
  const buttons = [...group.querySelectorAll('button[data-mode]')];
  const apply = (mode, save) => {
    document.body.dataset.mode = mode;
    for (const b of buttons) b.setAttribute('aria-pressed', String(b.dataset.mode === mode));
    for (const d of document.querySelectorAll('details.fellow')) d.open = mode === 'fellow';
    if (save) storage.set(MODE_KEY, mode);
  };
  for (const b of buttons) b.addEventListener('click', () => apply(b.dataset.mode, true));
  apply(storage.get(MODE_KEY) === 'fellow' ? 'fellow' : 'pgy', false);
  group.hidden = false;
}

// ---- 目錄、目前章節、複製連結 -------------------------------------------------
function initToc() {
  const details = document.querySelector('.toc-details');
  if (!details) return;
  if (narrowScreen.matches) details.open = false;
  // 桌面版隱藏 summary，若從手機寬度放大時目錄仍收合就再也打不開，所以寬度跨界時同步開合。
  narrowScreen.addEventListener('change', (event) => { details.open = !event.matches; });
  details.addEventListener('click', (event) => {
    if (event.target.closest('a') && narrowScreen.matches) details.open = false;
  });

  const links = new Map([...details.querySelectorAll('.toc-list a[href^="#"]')].map((a) => [a.hash.slice(1), a]));
  if (!('IntersectionObserver' in window)) return;
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      for (const a of links.values()) a.removeAttribute('aria-current');
      links.get(entry.target.id)?.setAttribute('aria-current', 'true');
    }
  }, { rootMargin: '0px 0px -70% 0px' });
  for (const id of links.keys()) {
    const section = document.getElementById(id);
    if (section) observer.observe(section);
  }
}

function initCopyLinks() {
  for (const button of document.querySelectorAll('.copy-link[data-target]')) {
    button.hidden = false;
    button.addEventListener('click', async () => {
      const url = `${location.origin}${location.pathname}${location.search}#${button.dataset.target}`;
      const original = button.textContent;
      try {
        await navigator.clipboard.writeText(url);
        button.textContent = '已複製';
      } catch {
        history.replaceState(null, '', `#${button.dataset.target}`);
        button.textContent = '已放到網址列';
      }
      setTimeout(() => { button.textContent = original; }, 2000);
    });
  }
}

// ---- 搜尋 -------------------------------------------------------------------
const normalize = (s) => s.normalize('NFKC').toLowerCase();

function buildSearchIndex() {
  const selector = '[data-search-title] :is(p, li, td, th, h3, legend, dd)';
  const excluded = '.quiz-answer, .calc, .sources, .section-tools, .legend, .options';
  const blocks = [...document.querySelectorAll(selector)].filter((node) => !node.closest(excluded)
    && !node.querySelector('p, li, td, th, h3, legend, dd'));
  return blocks.map((node) => {
    const text = node.textContent.replace(/\s+/g, ' ').trim();
    return {
      node,
      text,
      haystack: normalize(text),
      title: node.closest('[data-search-title]').dataset.searchTitle,
      target: node.closest('[id]'),
    };
  }).filter((entry) => entry.text && entry.target);
}

function snippetNodes(text, term) {
  const at = normalize(text).indexOf(term);
  const start = Math.max(0, at - 24);
  const end = Math.min(text.length, at + term.length + 40);
  const frag = document.createDocumentFragment();
  frag.append(`${start > 0 ? '…' : ''}${text.slice(start, at)}`);
  frag.append(el('mark', '', text.slice(at, at + term.length)));
  frag.append(`${text.slice(at + term.length, end)}${end < text.length ? '…' : ''}`);
  return frag;
}

function initSearch() {
  const box = document.querySelector('.search');
  const input = document.getElementById('site-search');
  const status = document.getElementById('search-status');
  const list = document.getElementById('search-results');
  if (!box || !input || !status || !list) return;
  let index = null;
  let timer;

  const run = () => {
    index ??= buildSearchIndex();
    const terms = normalize(input.value).split(/\s+/).filter(Boolean);
    list.replaceChildren();
    if (terms.length === 0) { status.textContent = ''; return; }
    const hits = index.filter((entry) => terms.every((t) => entry.haystack.includes(t)));
    status.textContent = hits.length ? `找到 ${hits.length} 處${hits.length > 30 ? '，顯示前 30 處' : ''}` : '找不到符合的內容';
    for (const hit of hits.slice(0, 30)) {
      const a = el('a');
      a.href = `#${hit.target.id}`;
      a.append(el('span', 'hit-title', hit.title), el('span', 'hit-text'));
      a.lastChild.append(snippetNodes(hit.text, terms[0]));
      a.addEventListener('click', () => openAncestors(hit.node));
      const li = el('li');
      li.append(a);
      list.append(li);
    }
  };

  input.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(run, 120); });
  input.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') { input.value = ''; run(); }
  });
  box.hidden = false;
}

// 從搜尋結果或外部連結跳到收合段落時，自動展開。
function revealHashTarget() {
  const id = decodeURIComponent(location.hash.slice(1));
  const target = id && document.getElementById(id);
  if (target) openAncestors(target);
}

// ---- 計算機 -----------------------------------------------------------------
function initCalculator() {
  const form = document.getElementById('calc-form');
  if (!form) return;
  const result = document.getElementById('calc-result');
  const flag = document.getElementById('calc-flag');
  const formError = document.getElementById('calc-form-error');

  const update = (focusOnError) => {
    const raw = Object.fromEntries(Object.keys(FIELDS).map((key) => [key, form.elements[key].value]));
    const outcome = computeInfusion(raw);
    const errors = outcome.ok ? {} : outcome.errors;
    for (const key of Object.keys(FIELDS)) {
      const input = form.elements[key];
      const message = document.getElementById(`calc-${key}-error`);
      input.setAttribute('aria-invalid', String(Boolean(errors[key])));
      message.textContent = errors[key] ?? '';
      message.hidden = !errors[key];
    }
    if (!outcome.ok) {
      const count = Object.keys(errors).length;
      formError.textContent = errors.form ?? `有 ${count} 個欄位需要修正，暫不顯示結果。`;
      formError.hidden = false;
      result.hidden = true;
      flag.hidden = true;
      if (focusOnError) form.querySelector('[aria-invalid="true"]')?.focus();
      return;
    }
    formError.hidden = true;
    const formatted = formatInfusion(outcome);
    for (const dd of result.querySelectorAll('[data-out]')) dd.textContent = formatted[dd.dataset.out];
    result.hidden = false;
    const { min, max } = LABEL_CONCENTRATION_U_PER_ML;
    flag.textContent = outcome.outsideLabelRange
      ? `濃度 ${formatted.concentration} 不在 NovoRapid EMA 仿單 IV 配製範圍（${min}–${max} U/mL）內：請核對產品與配製，這不是自動判定錯誤。`
      : '';
    flag.hidden = !outcome.outsideLabelRange;
  };

  form.addEventListener('submit', (event) => { event.preventDefault(); update(true); });
  form.addEventListener('change', () => update(false));
  form.addEventListener('reset', () => setTimeout(() => update(false), 0));
  form.hidden = false;
  update(false);
}

// ---- 測驗 -------------------------------------------------------------------
function initQuiz() {
  const items = [...document.querySelectorAll('.quiz-item[data-quiz-id]')].map((node) => ({
    node,
    id: node.dataset.quizId,
    answer: Number(node.dataset.answer),
    options: [...node.querySelectorAll('.option-text')].map((o) => o.textContent),
    radios: [...node.querySelectorAll('input[type="radio"]')],
    feedback: node.querySelector('.quiz-feedback'),
    reveal: node.querySelector('.quiz-answer'),
  }));
  if (items.length === 0) return;
  const bar = document.querySelector('.quiz-bar');
  const progress = document.getElementById('quiz-progress');
  const reset = document.getElementById('quiz-reset');
  let answers = restoreAnswers(storage.get(QUIZ_KEY), items);

  const showProgress = () => {
    const s = summarize(items, answers);
    progress.textContent = `已作答 ${s.answered} / ${s.total} · 答對 ${s.correct}`;
  };

  const show = (item, selected) => {
    const grade = gradeAnswer(item, selected);
    item.radios.forEach((radio, i) => {
      const label = radio.closest('.option');
      label.classList.toggle('is-correct', i === grade.correctIndex);
      label.classList.toggle('is-wrong', i === selected && !grade.correct);
    });
    const letter = item.node.querySelectorAll('.letter')[grade.correctIndex].textContent;
    item.feedback.className = `quiz-feedback ${grade.correct ? 'correct' : 'incorrect'}`;
    item.feedback.textContent = grade.correct ? '答對了。看看解析確認理由：' : `這個選項不對。正確答案是 ${letter}，理由如下：`;
    item.feedback.hidden = false;
    item.reveal.hidden = false;
    item.reveal.open = true;
  };

  const clear = (item) => {
    for (const radio of item.radios) {
      radio.checked = false;
      radio.closest('.option').classList.remove('is-correct', 'is-wrong');
    }
    item.feedback.hidden = true;
    item.feedback.textContent = '';
    item.reveal.open = false;
    item.reveal.hidden = true;
  };

  for (const item of items) {
    clear(item);
    if (Object.hasOwn(answers, item.id)) {
      item.radios[answers[item.id]].checked = true;
      show(item, answers[item.id]);
    }
    item.node.addEventListener('change', (event) => {
      if (!event.target.matches('input[type="radio"]')) return;
      const selected = Number(event.target.value);
      answers = { ...answers, [item.id]: selected };
      storage.set(QUIZ_KEY, JSON.stringify(answers));
      show(item, selected);
      showProgress();
    });
  }

  reset.addEventListener('click', () => {
    answers = {};
    storage.remove(QUIZ_KEY);
    items.forEach(clear);
    showProgress();
    items[0].radios[0].focus();
  });
  showProgress();
  bar.hidden = false;
}

// ---- 列印：展開所有段落與解析，印完恢復 ---------------------------------------
function initPrint() {
  let saved = [];
  window.addEventListener('beforeprint', () => {
    saved = [...document.querySelectorAll('details')].map((d) => [d, d.open, d.hidden]);
    for (const [d] of saved) { d.open = true; d.hidden = false; }
  });
  window.addEventListener('afterprint', () => {
    for (const [d, open, hidden] of saved) { d.open = open; d.hidden = hidden; }
    saved = [];
  });
}

initMode();
initToc();
initCopyLinks();
initSearch();
initCalculator();
initQuiz();
initPrint();
revealHashTarget();
window.addEventListener('hashchange', revealHashTarget);
