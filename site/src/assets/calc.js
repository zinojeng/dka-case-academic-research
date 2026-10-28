// Insulin 稀釋「算術校驗」：只把已知的配製與速率換算成單位，不提出任何速率或劑量建議。
// 同一份程式碼由瀏覽器（app.js）與 build/test（Node）共用，因此不可依賴 DOM。

export const FIELDS = {
  units: { label: 'Insulin 總量', unit: 'U', min: 1, max: 1000, example: '50' },
  volumeMl: { label: '稀釋總體積', unit: 'mL', min: 1, max: 5000, example: '500' },
  rateLowMlH: { label: '輸注速率（下限）', unit: 'mL/h', min: 0.1, max: 1000, example: '20' },
  rateHighMlH: { label: '輸注速率（上限）', unit: 'mL/h', min: 0.1, max: 1000, example: '30', optional: true },
  weightKg: { label: '體重', unit: 'kg', min: 20, max: 400, example: '104.5' },
};

// NovoRapid EMA 仿單的 IV 配製濃度範圍；只用來提示「請核對」，不是判定錯誤。
export const LABEL_CONCENTRATION_U_PER_ML = { min: 0.05, max: 1 };

// 只接受一般十進位數字：拒絕 1e3、0x10、逗號、負號、Infinity 這類容易誤讀的輸入。
const DECIMAL = /^\d{1,6}(?:\.\d{1,4})?$/;

export function parseField(raw, spec) {
  const text = String(raw ?? '').trim();
  if (text === '') {
    return spec.optional ? { value: null } : { error: `請輸入${spec.label}（${spec.unit}）。` };
  }
  if (!DECIMAL.test(text)) {
    return { error: `${spec.label}需為正數（例如 ${spec.example}），單位 ${spec.unit}；不接受負號、科學記號或其他符號。` };
  }
  const value = Number(text);
  if (!Number.isFinite(value) || value <= 0) {
    return { error: `${spec.label}必須大於 0 ${spec.unit}。` };
  }
  if (value < spec.min || value > spec.max) {
    return { error: `${spec.label}超出可信範圍（${spec.min}–${spec.max} ${spec.unit}），請確認輸入是否打錯。` };
  }
  return { value };
}

export function computeInfusion(raw = {}) {
  const values = {};
  const errors = {};
  for (const [key, spec] of Object.entries(FIELDS)) {
    const parsed = parseField(raw[key], spec);
    if ('error' in parsed) errors[key] = parsed.error;
    else values[key] = parsed.value;
  }
  if (!errors.rateLowMlH && !errors.rateHighMlH && values.rateHighMlH !== null && values.rateHighMlH < values.rateLowMlH) {
    errors.rateHighMlH = '速率上限需大於或等於下限。';
  }
  if (Object.keys(errors).length > 0) return { ok: false, errors };

  const concentration = values.units / values.volumeMl;
  const rateList = values.rateHighMlH === null || values.rateHighMlH === values.rateLowMlH
    ? [values.rateLowMlH]
    : [values.rateLowMlH, values.rateHighMlH];
  const rates = rateList.map((rateMlH) => {
    const unitsPerHour = rateMlH * concentration;
    return {
      rateMlH,
      unitsPerHour,
      unitsPerKgHour: unitsPerHour / values.weightKg,
      bagHours: values.volumeMl / rateMlH,
      vehicleMlPerDay: rateMlH * 24,
    };
  });
  const numbers = [concentration, ...rates.flatMap((r) => Object.values(r))];
  if (!numbers.every(Number.isFinite)) {
    return { ok: false, errors: { form: '計算結果不是有限數值，請檢查輸入。' } };
  }
  return {
    ok: true,
    values,
    concentration,
    outsideLabelRange: concentration < LABEL_CONCENTRATION_U_PER_ML.min || concentration > LABEL_CONCENTRATION_U_PER_ML.max,
    rates,
  };
}

// 以固定小數位四捨五入後去掉尾端 0：0.10 → "0.1"、2.00 → "2"、0.0287 → "0.029"。
export function formatNumber(value, decimals) {
  const fixed = value.toFixed(decimals);
  return fixed.includes('.') ? fixed.replace(/\.?0+$/, '') : fixed;
}

const joinRange = (items, decimals) => items.map((x) => formatNumber(x, decimals)).join(' / ');

export function formatInfusion(result) {
  const r = result.rates;
  return {
    concentration: `${formatNumber(result.concentration, 3)} U/mL`,
    rates: `${joinRange(r.map((x) => x.rateMlH), 1)} mL/h`,
    unitsPerHour: `${joinRange(r.map((x) => x.unitsPerHour), 2)} U/h`,
    unitsPerKgHour: `${joinRange(r.map((x) => x.unitsPerKgHour), 3)} U/kg/h`,
    bagHours: `${joinRange(r.map((x) => x.bagHours), 1)} h`,
    vehicleMlPerDay: `${joinRange(r.map((x) => x.vehicleMlPerDay), 0)} mL/day`,
  };
}
