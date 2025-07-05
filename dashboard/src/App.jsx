import { useEffect, useState } from 'react';
import './App.css';

// Column configs for renaming and type
const FEES_COLUMNS = [
  { key: 'protocol_name', label: 'Protocol', type: 'text' },
  { key: 'category', label: 'Category', type: 'text' },
  { key: 'fully_diluted_market_cap', label: 'FDV', type: 'usd', tooltip: 'Fully Diluted Valuation' },
  { key: 'fees_30d', label: 'Fees', type: 'usd', tooltip: 'Total protocol fees collected in the last 30 days (30d).' },
  { key: 'pf_ratio_forward_1y', label: 'P/F Ratio', type: 'ratio', tooltip: 'Price to Fees Ratio (Forward 1y): FDV / (30d Fees * 12)' },
  { key: 'fees_30d_change', label: 'Fees Change', type: 'percent', tooltip: 'Percent change in fees over the last 30 days (30d).' },
];
const REVENUE_COLUMNS = [
  { key: 'protocol_name', label: 'Protocol', type: 'text' },
  { key: 'category', label: 'Category', type: 'text' },
  { key: 'fully_diluted_market_cap', label: 'FDV', type: 'usd', tooltip: 'Fully Diluted Valuation' },
  { key: 'revenue_30d', label: 'Revenue', type: 'usd', tooltip: 'Total protocol revenue in the last 30 days (30d).' },
  { key: 'pr_ratio_forward_1y', label: 'P/R Ratio', type: 'ratio', tooltip: 'Price to Revenue Ratio (Forward 1y): FDV / (30d Revenue * 12)' },
  { key: 'revenue_30d_change', label: 'Revenue Change', type: 'percent', tooltip: 'Percent change in revenue over the last 30 days (30d).' },
];

function useTableData(url) {
  const [data, setData] = useState([]);
  useEffect(() => {
    fetch(url)
      .then((res) => res.json())
      .then(setData)
      .catch((err) => console.error('Failed to load', url, err));
  }, [url]);
  return data;
}

// Helper to format large numbers as 2.04T USD, 274.02B USD, etc.
function formatCompactUSD(value) {
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

// Helper to format percent change with color
function formatPercentChange(value) {
  if (value == null || isNaN(value)) return '';
  const color = value > 0 ? 'pos-change' : value < 0 ? 'neg-change' : '';
  const sign = value > 0 ? '+' : '';
  return <span className={`percent-change ${color}`}>{sign}{value.toFixed(2)}%</span>;
}

function Table({ columns, data }) {
  // Per-column filter state
  const [filters, setFilters] = useState(() =>
    Object.fromEntries(columns.map((col) => [col.key, ['usd', 'number', 'percent', 'ratio'].includes(col.type) ? { min: '', max: '' } : '']))
  );
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

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
      if (aVal === null || aVal === undefined) return 1;
      if (bVal === null || bVal === undefined) return -1;
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
    switch (col.type) {
      case 'usd':
        return (
          <span>
            {formatCompactUSD(value)} <span className="usd-label">USD</span>
          </span>
        );
      case 'percent': {
        if (value == null || isNaN(value)) return '';
        const color = value > 0 ? 'pos-change' : value < 0 ? 'neg-change' : '';
        const sign = value > 0 ? '+' : '';
        return <span className={`percent-change ${color}`}>{sign}{Number(value).toFixed(1)}%</span>;
      }
      case 'ratio':
        return value == null || isNaN(value) ? '--' : `${Number(value).toFixed(1)}x`;
      case 'number':
        return value == null || isNaN(value) ? '' : Number(value).toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 1 });
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
              {columns.map((col) => (
                <th
                  key={col.key}
                  onClick={() => handleSort(col.key)}
                  style={{ cursor: 'pointer', textAlign: 'center', position: 'relative' }}
                  tabIndex={0}
                >
                  <div className="header-main-label">
                    {col.label}{sortConfig.key === col.key ? (sortConfig.direction === 'asc' ? ' ▲' : ' ▼') : ''}
                    {col.tooltip && (
                      <span className="header-tooltip">&#9432;
                        <span className="header-tooltip-text">{col.tooltip}</span>
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
            {sortedData.map((row, i) => (
              <tr key={i}>
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

function App() {
  const feesData = useTableData('data/exports/fees_analysis.json');
  const revenueData = useTableData('data/exports/revenue_analysis.json');
  const [activeTab, setActiveTab] = useState('fees');
  // Removed lastUpdated state and fetch

  function formatDate(isoString) {
    if (!isoString) return '';
    const d = new Date(isoString);
    return d.toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
  }

  return (
    <div className="App">
      <h1>Protocol Fees/Revenue Screener</h1>
      {/* Removed last updated UI */}
      <div className="tabs">
        <button onClick={() => setActiveTab('fees')} className={activeTab === 'fees' ? 'active' : ''}>
          Fees
        </button>
        <button onClick={() => setActiveTab('revenue')} className={activeTab === 'revenue' ? 'active' : ''}>
          Revenue
        </button>
      </div>

      {activeTab === 'fees' && <Table columns={FEES_COLUMNS} data={feesData} />}
      {activeTab === 'revenue' && <Table columns={REVENUE_COLUMNS} data={revenueData} />}
    </div>
  );
}

export default App;
