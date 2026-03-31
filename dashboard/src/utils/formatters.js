export function formatCompactUSD(value) {
  if (value == null || isNaN(value)) return '';
  const abs = Math.abs(value);
  let num = value;
  let suffix = '';
  if (abs >= 1e12) {
    num = value / 1e12;
    suffix = 'T';
  } else if (abs >= 1e9) {
    num = value / 1e9;
    suffix = 'B';
  } else if (abs >= 1e6) {
    num = value / 1e6;
    suffix = 'M';
  } else if (abs >= 1e3) {
    num = value / 1e3;
    suffix = 'K';
  }
  return `${num.toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 1 })}${suffix}`;
}

export function formatPercentChange(value) {
  if (value == null || isNaN(value)) return { text: '', className: 'percent-change' };
  const color = value > 0 ? 'pos-change' : value < 0 ? 'neg-change' : '';
  const sign = value > 0 ? '+' : '';
  return { text: `${sign}${value.toFixed(2)}%`, className: `percent-change ${color}` };
}

export function formatRatio(value) {
  if (value == null || isNaN(value)) return '--';
  return `${Number(value).toFixed(1)}x`;
}

export function formatNumber(value) {
  if (value == null || isNaN(value)) return '';
  return Number(value).toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 1 });
}
