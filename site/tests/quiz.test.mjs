import test from 'node:test';
import assert from 'node:assert/strict';
import { gradeAnswer, restoreAnswers, summarize } from '../src/assets/quiz.js';

const QUIZZES = [
  { id: 'resolution', options: ['只看血糖', 'BOHB 加 pH/HCO3', '只看 anion gap'], answer: 1 },
  { id: 'potassium', options: ['照原速率', '先處理低鉀'], answer: 1 },
  { id: 'units', options: ['mg/dL', 'mmol/L'], answer: 0 },
];

test('gradeAnswer 回傳對錯與正確選項文字', () => {
  assert.deepEqual(gradeAnswer(QUIZZES[0], 1), { correct: true, selectedText: 'BOHB 加 pH/HCO3', correctIndex: 1, correctText: 'BOHB 加 pH/HCO3' });
  const wrong = gradeAnswer(QUIZZES[0], 2);
  assert.equal(wrong.correct, false);
  assert.equal(wrong.selectedText, '只看 anion gap');
  assert.equal(wrong.correctText, 'BOHB 加 pH/HCO3');
});

test('gradeAnswer 拒絕範圍外或非整數的選項', () => {
  for (const bad of [-1, 3, 1.5, NaN, '1']) assert.throws(() => gradeAnswer(QUIZZES[0], bad), RangeError);
});

test('summarize 只計算已作答的題目', () => {
  assert.deepEqual(summarize(QUIZZES, {}), { answered: 0, correct: 0, total: 3 });
  assert.deepEqual(summarize(QUIZZES, { resolution: 1, potassium: 0 }), { answered: 2, correct: 1, total: 3 });
  assert.deepEqual(summarize(QUIZZES, { resolution: 1, potassium: 1, units: 0, removed: 0 }), { answered: 3, correct: 3, total: 3 });
});

test('restoreAnswers 丟棄壞掉、過時或被竄改的紀錄', () => {
  assert.deepEqual(restoreAnswers(null, QUIZZES), {});
  assert.deepEqual(restoreAnswers('not json', QUIZZES), {});
  assert.deepEqual(restoreAnswers('[1,2]', QUIZZES), {});
  assert.deepEqual(restoreAnswers('null', QUIZZES), {});
  assert.deepEqual(
    restoreAnswers(JSON.stringify({ resolution: 2, potassium: 5, units: '0', removed: 1, __proto__: 1 }), QUIZZES),
    { resolution: 2 },
  );
});
