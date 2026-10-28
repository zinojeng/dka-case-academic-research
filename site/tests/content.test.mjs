import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { scanText, validateContent } from '../lib/validate.mjs';

const fixtureUrl = new URL('./fixtures/clinical.fixture.json', import.meta.url);
const realPath = fileURLToPath(new URL('../content/clinical.json', import.meta.url));
const fixture = () => JSON.parse(readFileSync(fixtureUrl, 'utf8'));

// 對 fixture 做一處修改，回傳錯誤訊息，方便斷言「這個錯誤確實被抓到」。
function errorsAfter(mutate) {
  const data = fixture();
  mutate(data);
  return validateContent(data).errors;
}

function assertCaught(mutate, pattern) {
  const errors = errorsAfter(mutate);
  assert.ok(errors.some((e) => pattern.test(e)), `預期錯誤 ${pattern}，實際：\n${errors.join('\n') || '(無錯誤)'}`);
}

test('fixture 符合契約', () => {
  assert.deepEqual(validateContent(fixture()).errors, []);
});

test('五題必須剛好是指定的 topic id', () => {
  assertCaught((d) => { d.topics = d.topics.filter((t) => t.id !== 'sodium'); }, /topics.*(至少需要 5 項|缺少題目：sodium)/);
  assertCaught((d) => { d.topics[1].id = 'magnesium'; }, /缺少題目：sodium/);
  assertCaught((d) => { d.topics.push({ ...d.topics[0], id: 'lipids' }); }, /未知題目 id：lipids/);
  assertCaught((d) => { d.topics[2].id = 'calcium-phosphate'; }, /重複的 id "calcium-phosphate"/);
});

test('quiz：至少 5 題、answer 在範圍內、來源可對應', () => {
  assertCaught((d) => { d.quizzes.pop(); }, /quizzes: 至少需要 5 項/);
  assertCaught((d) => { d.quizzes[0].answer = 2; }, /quizzes\[0\]\.answer/);
  assertCaught((d) => { d.quizzes[0].answer = '1'; }, /quizzes\[0\]\.answer/);
  assertCaught((d) => { d.quizzes[1].options = ['只有一個']; }, /quizzes\[1\]\.options: 至少需要 2 項/);
  assertCaught((d) => { d.quizzes[1].options = ['甲', '甲']; }, /選項重複/);
  assertCaught((d) => { d.quizzes[2].sourceIds = ['S99']; }, /來源 "S99" 不在 references/);
  assertCaught((d) => { d.quizzes[2].sourceIds = []; }, /至少需要 1 個來源/);
  assertCaught((d) => { d.quizzes[3].id = 'Q 4<'; }, /quizzes\[3\]\.id/);
  assertCaught((d) => { d.quizzes[4].id = 'q1'; }, /重複的 id "q1"/);
});

test('內文 [Sxx] 引用必須存在', () => {
  assertCaught((d) => { d.topics[0].body.push('沒有這個來源 [S77]。'); }, /引用 \[S77\]/);
  assertCaught((d) => { d.topics[0].fellow.push('2024 共識（S88 §4）'); }, /引用 \[S88\]/);
});

test('I/O 差值必須等於輸入減尿量', () => {
  assertCaught((d) => { d.io.differenceMl = 900; }, /io\.differenceMl.*896/);
  assertCaught((d) => { d.io.inputMl = '2946'; }, /io\.inputMl: 必須是數字/);
  assertCaught((d) => { d.io.urineMl = -1; d.io.differenceMl = 2947; }, /io\.urineMl: 不可為負數/);
});

test('timeline 必須涵蓋 Day 0、1、2', () => {
  assertCaught((d) => { d.timeline[2].day = 'Day 1 晚間'; }, /缺少 Day 2/);
  assertCaught((d) => { d.timeline[0].day = '入院日'; }, /必須以 Day 0/);
});

test('enum 與網址格式', () => {
  assertCaught((d) => { d.metrics[0].status = 'ok'; }, /metrics\[0\]\.status/);
  assertCaught((d) => { d.medications[0].evidence = 'given'; }, /medications\[0\]\.evidence/);
  assertCaught((d) => { d.references[0].url = 'http://doi.org/x'; }, /references\[0\]\.url/);
  assertCaught((d) => { d.references[0].id = 'ref-1'; }, /references\[0\]\.id/);
  // 非文獻來源（例如原廠產品頁）也必須登錄為 Sxx，不能另立前綴
  assertCaught((d) => { d.references.push({ id: 'P01', title: '原廠產品頁', url: 'https://example.org/p' }); }, /references\[3\]\.id: 格式需為 S/);
  assertCaught((d) => { d.updated = '2026/10/28'; }, /\$\.updated: 格式/);
});

test('缺欄位或空字串都會失敗，而不是渲染空白', () => {
  assertCaught((d) => { delete d.unknown; }, /\$\.unknown: 至少需要 1 項/);
  assertCaught((d) => { d.topics[0].fellow = []; }, /topics\[0\]\.fellow: 至少需要 1 項/);
  assertCaught((d) => { d.topics[0].takeaway = '  '; }, /topics\[0\]\.takeaway/);
  assertCaught((d) => { d.overview.push(''); }, /overview\[2\]/);
  assert.deepEqual(validateContent([]).errors, ['clinical.json 頂層必須是 object']);
});

test('placeholder 會讓 build 失敗', () => {
  assertCaught((d) => { d.topics[0].body[0] = 'TODO: 補內文'; }, /placeholder 標記/);
  assertCaught((d) => { d.known[0] = '待填'; }, /中文 placeholder/);
  assertCaught((d) => { d.overview[0] = 'This is demo data'; }, /"demo"/);
  assertCaught((d) => { d.quizzes[0].explanation = 'Lorem ipsum dolor'; }, /lorem ipsum/);
});

test('隱私：病歷號、真實日期、精確年齡、本機路徑、內部檔名都會被擋', () => {
  assertCaught((d) => { d.overview[0] = '病人 1234567 入院'; }, /6 位以上連續數字/);
  assertCaught((d) => { d.overview[0] = '病歷號見檔案'; }, /病歷號字樣/);
  assertCaught((d) => { d.timeline[0].items[0] = '2026-10-21 入院'; }, /完整日期 "2026-10-21"/);
  assertCaught((d) => { d.timeline[0].items[0] = '2026年10月21日 入院'; }, /完整日期/);
  assertCaught((d) => { d.overview[0] = '查核日期 2026-10-28'; }, /\$\.overview\[0\]: 完整日期 "2026-10-28"/);
  assertCaught((d) => { d.overview[0] = '42 歲男性'; }, /精確年齡/);
  assertCaught((d) => { d.overview[0] = 'a 42M with DKA'; }, /精確年齡/);
  assertCaught((d) => { d.overview[0] = '見 /Users/someone/case'; }, /本機絕對路徑/);
  assertCaught((d) => { d.overview[0] = '見 C:\\cases\\x'; }, /本機絕對路徑/);
  assertCaught((d) => { d.overview[0] = '詳見 .private/case-brief'; }, /內部 workflow 路徑/);
  assertCaught((d) => { d.overview[0] = '詳見 clinical-summary.zh-TW.md'; }, /Markdown 檔名/);
  assertCaught((d) => { d.overview[0] = '依 workflow.py 的 manifest'; }, /內部 workflow 紀錄/);
});

test('隱私掃描不誤傷正常臨床文字', () => {
  for (const ok of [
    '40 多歲男性，Day 1 15:03 K 3.2 mmol/L。',
    '查核日期 2026-10-28。',
    'Na 122 vs 131；glucose 411 mg/dL；TG 1950 mg/dL。',
    'clinical manifestation 與 0.019 U/kg/h。',
    '0.1 U/mL × 20 mL/h = 2 U/h。',
  ]) {
    assert.deepEqual(scanText(ok, { allowedDates: ['2026-10-28'] }), [], ok);
  }
  // 文獻標題中的 article number 不是病歷號
  assert.deepEqual(errorsAfter((d) => { d.references[2].title = 'JAMA Netw Open 2020;3:e2024596.'; }), []);
});

test('交付的 site/content/clinical.json 符合契約', (t) => {
  if (!existsSync(realPath)) {
    t.skip('content/clinical.json 尚未交付；build 會因此失敗');
    return;
  }
  const { errors } = validateContent(JSON.parse(readFileSync(realPath, 'utf8')));
  assert.deepEqual(errors, []);
});
