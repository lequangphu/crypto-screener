import { useState, useRef } from 'react';
import { TooltipPortal } from './TooltipPortal';
import { formatCompactUSD, formatPercentChange, formatRatio, formatNumber } from '../utils/formatters';

export function Table({ columns, data, sparklines = {} }) {
  // Per-column filter state
  const [filters, setFilters] = useState(() =>
    Object.fromEntries(columns.map((col) => [col.key, ['usd', 'number', 'percent', 'ratio'].includes(col.type) ? { min: '', max: '' } : '']))
  );
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [tooltip, setTooltip] = useState({ idx: null, visible: false });
  const tooltipAnchorRefs = useRef([]);

  // Filtering logic
  const filteredData = data.filter((row) =>
    columns.every((col) => {
      if (col.type === 'text') {
        const val = (row[col.key] ?? '').toString().toLowerCase();
        const filterVal = (filters[col.key] ?? '').toLowerCase();
        return val.includes(filterVal);
      } else if (["usd", "number", "percent", "ratio"].includes(col.type)) {
        const valRaw = row[col.key];
        const val = Number(valRaw);
        const { min, max } = filters[col.key] || {};
        const minVal = Number(min);
        const maxVal = Number(max);
        // If min or max is set, exclude empty/null/undefined/NaN
        if ((min !== '' || max !== '') && (valRaw === null || valRaw === undefined || valRaw === '' || isNaN(val))) {
          return false;
        }
        if (min !== '' && !isNaN(minVal) && val < minVal) return false;
        if (max !== '' && !isNaN(maxVal) && val > maxVal) return false;
        return true;
      }
      return true;
    })
  );

  // Sorting logic
  const sortedData = [...filteredData];
  if (sortConfig.key) {
    sortedData.sort((a, b) => {
      const aVal = a[sortConfig.key];
      const bVal = b[sortConfig.key];
      if (aVal === bVal) return 0;
      // Handle null, undefined, and NaN values consistently
      const aInvalid = aVal === null || aVal === undefined || (typeof aVal === 'number' && isNaN(aVal));
      const bInvalid = bVal === null || bVal === undefined || (typeof bVal === 'number' && isNaN(bVal));
      if (aInvalid && bInvalid) return 0;
      if (aInvalid) return 1;
      if (bInvalid) return -1;
      const col = columns.find(c => c.key === sortConfig.key);
      if (col && ["usd", "number", "percent", "ratio"].includes(col.type)) {
        return sortConfig.direction === 'asc' ? Number(aVal) - Number(bVal) : Number(bVal) - Number(aVal);
      }
      return sortConfig.direction === 'asc'
        ? String(aVal).localeCompare(String(bVal))
        : String(bVal).localeCompare(String(aVal));
    });
  }

  const handleSort = (col) => {
    setSortConfig((prev) => {
      if (prev.key === col) {
        return { key: col, direction: prev.direction === 'asc' ? 'desc' : 'asc' };
      }
      return { key: col, direction: 'asc' };
    });
  };

  const handleFilterChange = (col, value, bound) => {
    setFilters((prev) => {
      if (bound) {
        return { ...prev, [col]: { ...prev[col], [bound]: value } };
      }
      return { ...prev, [col]: value };
    });
  };

  function renderCell(col, value, row) {
    // Check if this column should have sparkline
    const sparklineData = sparklines[row.protocol_name]?.[col.key];

    switch (col.type) {
      case 'usd':
        return (
          <span>
            {formatCompactUSD(value)} <span className="usd-label">USD</span>
            {sparklineData && (
              <span className="sparkline-cell">
                {/* Sparkline will be rendered here by parent */}
              </span>
            )}
          </span>
        );
      case 'percent': {
        const formatted = formatPercentChange(value);
        if (!formatted.text) return '';
        return <span className={formatted.className}>{formatted.text}</span>;
      }
      case 'ratio':
        return formatRatio(value);
      case 'number':
        return formatNumber(value);
      case 'text':
      default:
        // Hyperlink protocol_name if slug is available
        if (col.key === 'protocol_name' && row && row.slug) {
          return (
            <a href={`https://defillama.com/protocol/${row.slug}`} target="_blank" rel="noopener noreferrer">
              {value}
            </a>
          );
        }
        return value != null ? value.toString() : '';
    }
  }

  return (
    <div style={{ marginBottom: 48 }}>
      <div style={{ overflowX: 'auto' }}>
        <table>
          <thead>
            <tr>
              {columns.map((col, idx) => (
                <th
                  key={col.key}
                  onClick={() => handleSort(col.key)}
                  style={{ cursor: 'pointer', textAlign: 'center', position: 'relative' }}
                  tabIndex={0}
                >
                  <div className="header-main-label">
                    {col.label}{sortConfig.key === col.key ? (sortConfig.direction === 'asc' ? ' ▲' : ' ▼') : ''}
                    {col.tooltip && (
                      <span
                        className="header-tooltip"
                        ref={el => (tooltipAnchorRefs.current[idx] = el)}
                        onMouseEnter={() => setTooltip({ idx, visible: true })}
                        onMouseLeave={() => setTooltip({ idx: null, visible: false })}
                        onFocus={() => setTooltip({ idx, visible: true })}
                        onBlur={() => setTooltip({ idx: null, visible: false })}
                        tabIndex={0}
                        aria-label={col.tooltip}
                      >
                        &#9432;
                        {tooltip.visible && tooltip.idx === idx && (
                          <TooltipPortal anchorRef={{ current: tooltipAnchorRefs.current[idx] }} visible={true}>
                            {col.tooltip}
                          </TooltipPortal>
                        )}
                      </span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
            <tr>
              {columns.map((col) => (
                <th key={col.key} style={{ textAlign: ['usd', 'number', 'percent', 'ratio'].includes(col.type) ? 'right' : 'left' }}>
                  {col.type === 'text' ? (
                    <input
                      type="text"
                      value={filters[col.key]}
                      onChange={(e) => handleFilterChange(col.key, e.target.value)}
                      placeholder="Filter"
                      style={{ width: 100 }}
                    />
                  ) : (
                    <div style={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                      <input
                        type="text"
                        value={filters[col.key].min}
                        onChange={(e) => handleFilterChange(col.key, e.target.value, 'min')}
                        placeholder="Min"
                        style={{ width: 70 }}
                      />
                      <input
                        type="text"
                        value={filters[col.key].max}
                        onChange={(e) => handleFilterChange(col.key, e.target.value, 'max')}
                        placeholder="Max"
                        style={{ width: 70 }}
                      />
                    </div>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sortedData.map((row) => (
              <tr key={row.slug || row.protocol_name || JSON.stringify(row)}>
                {columns.map((col) => (
                  <td
                    key={col.key}
                    style={{ textAlign: ['usd', 'number', 'percent', 'ratio'].includes(col.type) ? 'right' : 'left', whiteSpace: 'nowrap' }}
                  >
                    {renderCell(col, row[col.key], row)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p style={{ marginTop: 8, fontSize: 12, color: '#888' }}>
        Click column headers to sort. Filter each column individually. Numeric columns support min/max. Use scientific notation (e.g. 1e9) for large numbers.
      </p>
      <p style={{ marginTop: 4, fontSize: 12, color: '#888' }}>
        <strong>Note:</strong> Forward P/F and P/R ratios are calculated as <code>FDV / (30d Fees/Revenue * 12)</code>.
      </p>
    </div>
  );
}
