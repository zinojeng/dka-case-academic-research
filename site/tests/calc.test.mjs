import test from 'node:test';
import assert from 'node:assert/strict';
import { computeInfusion, formatInfusion, formatNumber } from '../src/assets/calc.js';

const CASE = { units: '50', volumeMl: '500', rateLowMlH: '20', rateHighMlH: '30', weightKg: '104.5' };

test('本例：50 U / 500 mL、20–30 mL/h、104.5 kg', () => {
  const r = computeInfusion(CASE);
  assert.equal(r.ok, true);
  assert.equal(r.concentration, 0.1);
  assert.deepEqual(r.rates.map((x) => x.unitsPerHour), [2, 3]);
  // 2 / 104.5 = 0.019138…、3 / 104.5 = 0.028708…
  assert.ok(Math.abs(r.rates[0].unitsPerKgHour - 0.0191388) < 1e-6);
  assert.ok(Math.abs(r.rates[1].unitsPerKgHour - 0.0287081) < 1e-6);
  assert.deepEqual(r.rates.map((x) => x.bagHours), [25, 500 / 30]);
  assert.deepEqual(r.rates.map((x) => x.vehicleMlPerDay), [480, 720]);
  assert.equal(r.outsideLabelRange, false);
});

test('格式化輸出與教學頁一致', () => {
  assert.deepEqual(formatInfusion(computeInfusion(CASE)), {
    concentration: '0.1 U/mL',
    rates: '20 / 30 mL/h',
    unitsPerHour: '2 / 3 U/h',
    unitsPerKgHour: '0.019 / 0.029 U/kg/h',
    bagHours: '25 / 16.7 h',
    vehicleMlPerDay: '480 / 720 mL/day',
  });
});

test('上限空白或與下限相同時只算一個速率', () => {
  for (const high of ['', '20']) {
    const r = computeInfusion({ ...CASE, rateHighMlH: high });
    assert.equal(r.ok, true);
    assert.equal(r.rates.length, 1);
    assert.equal(formatInfusion(r).unitsPerHour, '2 U/h');
  }
});

test('拒絕 0、負數、NaN、Infinity、科學記號、hex、空白與千分位', () => {
  for (const bad of ['0', '0.0', '-5', 'abc', 'NaN', 'Infinity', '1e3', '0x10', '', '   ', '1,000', '5.', '.5']) {
    const r = computeInfusion({ ...CASE, units: bad });
    assert.equal(r.ok, false, `units=${JSON.stringify(bad)} 應被拒絕`);
    assert.match(r.errors.units, /Insulin 總量/);
    assert.deepEqual(Object.keys(r.errors), ['units'], '只有出錯的欄位有錯誤訊息');
  }
});

test('拒絕不合理或會溢位的大數', () => {
  assert.match(computeInfusion({ ...CASE, units: '9999999' }).errors.units, /正數/); // 超過 6 位整數
  assert.match(computeInfusion({ ...CASE, volumeMl: '5001' }).errors.volumeMl, /5000 mL/);
  assert.match(computeInfusion({ ...CASE, weightKg: '1000' }).errors.weightKg, /20–400 kg/);
  assert.match(computeInfusion({ ...CASE, weightKg: '5' }).errors.weightKg, /kg/);
  assert.match(computeInfusion({ ...CASE, rateLowMlH: '0.05' }).errors.rateLowMlH, /mL\/h/);
});

test('速率上限小於下限時報錯，不默默交換', () => {
  const r = computeInfusion({ ...CASE, rateLowMlH: '30', rateHighMlH: '20' });
  assert.equal(r.ok, false);
  assert.match(r.errors.rateHighMlH, /上限需大於或等於下限/);
});

test('缺欄位（undefined）視為未輸入', () => {
  const r = computeInfusion({ units: '50' });
  assert.equal(r.ok, false);
  assert.deepEqual(Object.keys(r.errors).sort(), ['rateLowMlH', 'volumeMl', 'weightKg']);
});

test('反推一致：U/kg/h × 體重 × 體積 ÷ 總單位 = mL/h', () => {
  const samples = [
    ['100', '100', '7.5', '', '62.3'],
    ['25', '250', '1', '12', '20'],
    ['1000', '5000', '0.1', '1000', '400'],
    ['50', '50', '3.25', '4', '88.8'],
  ];
  for (const [units, volumeMl, rateLowMlH, rateHighMlH, weightKg] of samples) {
    const r = computeInfusion({ units, volumeMl, rateLowMlH, rateHighMlH, weightKg });
    assert.equal(r.ok, true);
    for (const rate of r.rates) {
      const back = (rate.unitsPerKgHour * Number(weightKg) * Number(volumeMl)) / Number(units);
      assert.ok(Math.abs(back - rate.rateMlH) < 1e-9, `${back} vs ${rate.rateMlH}`);
      assert.ok(Math.abs(rate.bagHours * rate.rateMlH - Number(volumeMl)) < 1e-9);
    }
  }
});

test('濃度超出 EMA IV 配製範圍時只提示核對', () => {
  assert.equal(computeInfusion({ ...CASE, units: '100', volumeMl: '50' }).outsideLabelRange, true); // 2 U/mL
  assert.equal(computeInfusion({ ...CASE, units: '10', volumeMl: '500' }).outsideLabelRange, true); // 0.02 U/mL
  assert.equal(computeInfusion({ ...CASE, units: '25', volumeMl: '500' }).outsideLabelRange, false); // 0.05 U/mL 邊界
});

test('formatNumber 去尾零但保留必要位數', () => {
  assert.equal(formatNumber(0.1, 3), '0.1');
  assert.equal(formatNumber(2, 2), '2');
  assert.equal(formatNumber(16.666, 1), '16.7');
  assert.equal(formatNumber(480, 0), '480');
  assert.equal(formatNumber(100, 0), '100');
  assert.equal(formatNumber(0.0287, 3), '0.029');
});
