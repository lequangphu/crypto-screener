import { describe, it, expect } from 'vitest'
import { formatCompactUSD, formatPercentChange, formatRatio, formatNumber } from '../utils/formatters'

describe('formatCompactUSD', () => {
  it('formats trillions with T suffix', () => {
    expect(formatCompactUSD(2000000000000)).toBe('2.0T')
    expect(formatCompactUSD(2500000000000)).toBe('2.5T')
  })

  it('formats billions with B suffix', () => {
    expect(formatCompactUSD(1000000000)).toBe('1.0B')
    expect(formatCompactUSD(274000000000)).toBe('274.0B')
  })

  it('formats millions with M suffix', () => {
    expect(formatCompactUSD(1000000)).toBe('1.0M')
    expect(formatCompactUSD(5000000)).toBe('5.0M')
  })

  it('formats thousands with K suffix', () => {
    expect(formatCompactUSD(1000)).toBe('1.0K')
    expect(formatCompactUSD(2500)).toBe('2.5K')
  })

  it('handles small numbers without suffix', () => {
    expect(formatCompactUSD(500)).toBe('500.0')
    expect(formatCompactUSD(0)).toBe('0.0')
  })

  it('handles null and NaN values', () => {
    expect(formatCompactUSD(null)).toBe('')
    expect(formatCompactUSD(undefined)).toBe('')
    expect(formatCompactUSD(NaN)).toBe('')
  })

  it('handles negative values', () => {
    expect(formatCompactUSD(-1000000)).toBe('-1.0M')
    expect(formatCompactUSD(-1000000000)).toBe('-1.0B')
  })
})

describe('formatPercentChange', () => {
  it('formats positive values with + sign and pos-change class', () => {
    const result = formatPercentChange(5.5)
    expect(result.text).toBe('+5.50%')
    expect(result.className).toContain('pos-change')
  })

  it('formats negative values with neg-change class', () => {
    const result = formatPercentChange(-3.25)
    expect(result.text).toBe('-3.25%')
    expect(result.className).toContain('neg-change')
  })

  it('formats zero without color class', () => {
    const result = formatPercentChange(0)
    expect(result.text).toBe('0.00%')
    expect(result.className).not.toContain('pos-change')
    expect(result.className).not.toContain('neg-change')
  })

  it('handles null and NaN values', () => {
    expect(formatPercentChange(null).text).toBe('')
    expect(formatPercentChange(undefined).text).toBe('')
    expect(formatPercentChange(NaN).text).toBe('')
  })
})

describe('formatRatio', () => {
  it('formats ratios with x suffix', () => {
    expect(formatRatio(15.5)).toBe('15.5x')
    expect(formatRatio(2.1)).toBe('2.1x')
  })

  it('handles null and NaN values', () => {
    expect(formatRatio(null)).toBe('--')
    expect(formatRatio(undefined)).toBe('--')
    expect(formatRatio(NaN)).toBe('--')
  })

  it('rounds to one decimal place', () => {
    expect(formatRatio(15.55)).toBe('15.6x')
    expect(formatRatio(15.54)).toBe('15.5x')
  })
})

describe('formatNumber', () => {
  it('formats numbers with locale string', () => {
    expect(formatNumber(1234.5)).toBe('1,234.5')
    expect(formatNumber(1000000)).toBe('1,000,000.0')
  })

  it('handles null and NaN values', () => {
    expect(formatNumber(null)).toBe('')
    expect(formatNumber(undefined)).toBe('')
    expect(formatNumber(NaN)).toBe('')
  })

  it('formats to one decimal place', () => {
    expect(formatNumber(123.456)).toBe('123.5')
    expect(formatNumber(123.454)).toBe('123.5')
  })
})
