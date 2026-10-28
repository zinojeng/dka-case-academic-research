// clinical.json 契約檢查＋公開內容的隱私／placeholder 掃描。
// 任何 error 都讓 build 失敗：缺資料時寧可不出站，也不要假成功。

export const TOPIC_IDS = ['calcium-phosphate', 'sodium', 'potassium', 'fluids', 'insulin'];
export const METRIC_STATUS = ['known', 'caution', 'unknown'];
export const MED_EVIDENCE = ['order', 'user-confirmed', 'recorded'];
export const MIN_QUIZZES = 5;

const PLACEHOLDER = [
  [/\b(?:TODO|TBD|FIXME|XXX)\b/, 'placeholder 標記'],
  [/lorem ipsum/i, 'lorem ipsum'],
  [/placeholder/i, '"placeholder"'],
  [/\bdemo\b/i, '"demo"'],
  [/佔位|占位|待填|範例文字/, '中文 placeholder'],
  [/\?\?\?/, '"???"'],
];

const PRIVACY = [
  [/(?:^|[\s("'`])(?:\/Users\/|\/home\/|\/private\/|~\/)|[A-Za-z]:\\|file:\/\//, '本機絕對路徑'],
  [/(?:^|[\s/("'`])\.private\b|\b(?:runtime|sessions|coordination|parsed|fulltext)\/[\w.-]/, '內部 workflow 路徑'],
  [/[\w.-]+\.md\b/i, 'Markdown 檔名（可能是原始病歷或內部報告）'],
  [/病歷號|\bMRN\b|chart\s*(?:no|number)|medical record number/i, '病歷號字樣'],
  [/(?:^|\D)42\s*(?:歲|y\/?o\b|-?year|M\b)|四十二歲/i, '精確年齡（公開版請寫 40 多歲）'],
  [/workflow\.py|\bmanifests?\b|\bmailbox\b|session[-_ ]?(?:id|log)/i, '內部 workflow 紀錄'],
];

// 文獻標題常有 e2024596 這種 article number，所以這條只用在非 references 欄位。
const LONG_NUMBER = [/(?:^|\D)\d{6,}(?!\d)/, '6 位以上連續數字（可能是病歷號）'];

// 完整日期（年-月-日）一律視為可能的真實個案日期；只放行明確允許的查核日期。
const FULL_DATE = /(?:19|20)\d{2}\s*[-/.年]\s*\d{1,2}\s*[-/.月]\s*\d{1,2}/g;

// 給 build 檢查產出 HTML（含屬性）用：回傳所有完整日期字串。
export function findFullDates(text) {
  return [...text.matchAll(FULL_DATE)].map((m) => m[0]);
}

function normalizeDate(text) {
  const [y, m, d] = text.match(/\d+/g);
  return `${y}-${m.padStart(2, '0')}-${d.padStart(2, '0')}`;
}

// 掃描單一字串；url 欄位另外檢查，因為 DOI 本身就含長串數字。
export function scanText(text, { allowedDates = [], allowLongNumbers = false } = {}) {
  const problems = [];
  for (const [re, label] of [...PLACEHOLDER, ...PRIVACY, ...(allowLongNumbers ? [] : [LONG_NUMBER])]) {
    if (re.test(text)) problems.push(label);
  }
  for (const match of text.matchAll(FULL_DATE)) {
    if (!allowedDates.includes(normalizeDate(match[0]))) problems.push(`完整日期 "${match[0]}"（可能是真實個案日期）`);
  }
  return problems;
}

function* stringLeaves(value, path) {
  if (typeof value === 'string') yield [path, value];
  else if (Array.isArray(value)) for (const [i, v] of value.entries()) yield* stringLeaves(v, `${path}[${i}]`);
  else if (value && typeof value === 'object') for (const [k, v] of Object.entries(value)) yield* stringLeaves(v, `${path}.${k}`);
}

const isObject = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);
const isText = (v) => typeof v === 'string' && v.trim().length > 0;

export function validateContent(data) {
  const errors = [];
  const fail = (path, message) => errors.push(`${path}: ${message}`);

  if (!isObject(data)) return { errors: ['clinical.json 頂層必須是 object'] };

  const text = (obj, key, path) => {
    if (!isText(obj?.[key])) fail(`${path}.${key}`, '必須是非空字串');
  };
  const textList = (obj, key, path, min = 1) => {
    const list = obj?.[key];
    if (!Array.isArray(list) || list.length < min) return fail(`${path}.${key}`, `至少需要 ${min} 項`);
    list.forEach((item, i) => { if (!isText(item)) fail(`${path}.${key}[${i}]`, '必須是非空字串'); });
  };
  const objectList = (key, min, check) => {
    const list = data[key];
    if (!Array.isArray(list) || list.length < min) return fail(key, `至少需要 ${min} 項`);
    list.forEach((item, i) => (isObject(item) ? check(item, `${key}[${i}]`) : fail(`${key}[${i}]`, '必須是 object')));
  };
  const uniqueIds = (key) => {
    const seen = new Set();
    for (const [i, item] of (Array.isArray(data[key]) ? data[key] : []).entries()) {
      if (!isText(item?.id)) continue;
      if (seen.has(item.id)) fail(`${key}[${i}].id`, `重複的 id "${item.id}"`);
      seen.add(item.id);
    }
    return seen;
  };

  for (const key of ['title', 'audience', 'updated']) text(data, key, '$');
  if (isText(data.updated) && !/^\d{4}-\d{2}-\d{2}$/.test(data.updated)) fail('$.updated', '格式需為 YYYY-MM-DD');
  textList(data, 'overview', '$');
  textList(data, 'known', '$');
  textList(data, 'unknown', '$');

  objectList('references', 3, (ref, path) => {
    text(ref, 'id', path);
    text(ref, 'title', path);
    if (isText(ref.id) && !/^S\d{2,3}$/.test(ref.id)) fail(`${path}.id`, '格式需為 S 加 2–3 位數字（例如 S02），需對應 evidence/source-register.json');
    if (!isText(ref.url) || !/^https:\/\/[^\s<>"']+$/.test(ref.url)) fail(`${path}.url`, '必須是 https:// 開頭、不含空白的網址');
  });
  const refIds = uniqueIds('references');
  const checkSources = (item, path) => {
    if (!Array.isArray(item.sourceIds) || item.sourceIds.length === 0) return fail(`${path}.sourceIds`, '至少需要 1 個來源');
    for (const id of item.sourceIds) if (!refIds.has(id)) fail(`${path}.sourceIds`, `來源 "${id}" 不在 references 中`);
  };

  objectList('metrics', 1, (m, path) => {
    for (const key of ['label', 'value']) text(m, key, path);
    for (const key of ['unit', 'note']) if (m[key] !== undefined && typeof m[key] !== 'string') fail(`${path}.${key}`, '必須是字串');
    if (!METRIC_STATUS.includes(m.status)) fail(`${path}.status`, `必須是 ${METRIC_STATUS.join(' | ')}`);
  });

  objectList('topics', TOPIC_IDS.length, (t, path) => {
    for (const key of ['id', 'title', 'summary', 'takeaway']) text(t, key, path);
    textList(t, 'body', path);
    textList(t, 'fellow', path);
    checkSources(t, path);
  });
  const topicIds = uniqueIds('topics');
  const missingTopics = TOPIC_IDS.filter((id) => !topicIds.has(id));
  const extraTopics = [...topicIds].filter((id) => !TOPIC_IDS.includes(id));
  if (missingTopics.length) fail('topics', `缺少題目：${missingTopics.join(', ')}`);
  if (extraTopics.length) fail('topics', `未知題目 id：${extraTopics.join(', ')}（只允許 ${TOPIC_IDS.join(', ')}）`);

  objectList('timeline', 3, (d, path) => {
    text(d, 'day', path);
    text(d, 'title', path);
    textList(d, 'items', path);
    if (isText(d.day) && !/^Day ?[0-2](?!\d)/.test(d.day)) fail(`${path}.day`, '必須以 Day 0 / Day 1 / Day 2 開頭');
  });
  const days = new Set((data.timeline ?? []).map((d) => String(d?.day ?? '').match(/^Day ?([0-2])/)?.[1]).filter(Boolean));
  for (const d of ['0', '1', '2']) if (Array.isArray(data.timeline) && !days.has(d)) fail('timeline', `缺少 Day ${d}`);

  objectList('medications', 1, (m, path) => {
    for (const key of ['name', 'order', 'teaching']) text(m, key, path);
    if (!MED_EVIDENCE.includes(m.evidence)) fail(`${path}.evidence`, `必須是 ${MED_EVIDENCE.join(' | ')}`);
  });

  if (!isObject(data.io)) fail('io', '必須是 object');
  else {
    text(data.io, 'label', 'io');
    for (const key of ['inputMl', 'urineMl', 'differenceMl']) {
      const v = data.io[key];
      if (!Number.isFinite(v)) fail(`io.${key}`, '必須是數字');
      else if (key !== 'differenceMl' && v < 0) fail(`io.${key}`, '不可為負數');
    }
    if ([data.io.inputMl, data.io.urineMl, data.io.differenceMl].every(Number.isFinite)
      && Math.abs(data.io.inputMl - data.io.urineMl - data.io.differenceMl) > 0.5) {
      fail('io.differenceMl', `與 inputMl − urineMl（${data.io.inputMl - data.io.urineMl}）不一致`);
    }
    textList(data.io, 'caveats', 'io');
  }

  objectList('quizzes', MIN_QUIZZES, (q, path) => {
    for (const key of ['id', 'question', 'explanation']) text(q, key, path);
    if (isText(q.id) && !/^[a-z0-9][a-z0-9-]*$/.test(q.id)) fail(`${path}.id`, '只能用小寫英數與連字號（會用在 HTML id）');
    textList(q, 'options', path, 2);
    if (Array.isArray(q.options) && new Set(q.options).size !== q.options.length) fail(`${path}.options`, '選項重複');
    if (!Number.isInteger(q.answer) || q.answer < 0 || q.answer >= (q.options?.length ?? 0)) fail(`${path}.answer`, '必須是 options 範圍內的整數 index');
    checkSources(q, path);
  });
  uniqueIds('quizzes');

  // 內文的 S02 / [S02] 形式引用也要能對到 references。
  for (const [path, value] of stringLeaves(data, '$')) {
    if (path.endsWith('.url')) continue;
    if (!path.startsWith('$.references')) {
      for (const [, id] of value.matchAll(/(?<![\w-])(S\d{2,3})(?!\w)/g)) if (!refIds.has(id)) fail(path, `引用 [${id}] 不在 references 中`);
    }
    // updated 是唯一允許的完整日期，而且只作為輸入；公開頁只顯示年月，所以其他欄位不可寫完整日期。
    const options = { allowedDates: path === '$.updated' ? [value] : [], allowLongNumbers: path.startsWith('$.references') };
    for (const problem of scanText(value, options)) fail(path, problem);
  }

  return { errors };
}
