import { useEffect, useState } from 'react';
import './App.css';

// Column configs for renaming and type
const FEES_COLUMNS = [
  { key: 'protocol_name', label: 'Protocol', type: 'text' },
  { key: 'category', label: 'Category', type: 'text' },
  { key: 'fully_diluted_market_cap', label: 'FDV', type: 'fdv_million' },
  { key: 'fees_30d', label: 'Fees (30d)', type: 'currency' },
  { key: 'fees_30d_change', label: 'Fees 30d Change', type: 'number' },
  { key: 'pf_ratio_forward_1y', label: 'P/F Ratio (Forward 1y)', type: 'ratio' },
];
const REVENUE_COLUMNS = [
  { key: 'protocol_name', label: 'Protocol', type: 'text' },
  { key: 'category', label: 'Category', type: 'text' },
  { key: 'fully_diluted_market_cap', label: 'FDV', type: 'fdv_million' },
  { key: 'revenue_30d', label: 'Revenue (30d)', type: 'currency' },
  { key: 'revenue_30d_change', label: 'Revenue 30d Change', type: 'number' },
  { key: 'pr_ratio_forward_1y', label: 'P/R Ratio (Forward 1y)', type: 'ratio' },
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
  return `${num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}${suffix}`;
}

// Helper to format percent change with color
function formatPercentChange(value) {
  if (value == null || isNaN(value)) return '';
  const color = value > 0 ? 'pos-change' : value < 0 ? 'neg-change' : '';
  const sign = value > 0 ? '+' : '';
  return <span className={`percent-change ${color}`}><b>{sign}{value.toFixed(2)}%</b></span>;
}

function Table({ columns, data }) {
  // Per-column filter state
  const [filters, setFilters] = useState(() =>
    Object.fromEntries(columns.map((col) => [col.key, col.type === 'number' || col.type === 'currency' ? { min: '', max: '' } : '']))
  );
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

  // Filtering logic
  const filteredData = data.filter((row) =>
    columns.every((col) => {
      if (col.type === 'text') {
        const val = (row[col.key] ?? '').toString().toLowerCase();
        const filterVal = (filters[col.key] ?? '').toLowerCase();
        return val.includes(filterVal);
      } else if (col.type === 'number' || col.type === 'currency') {
        const val = Number(row[col.key]);
        const { min, max } = filters[col.key] || {};
        if (min !== '' && !isNaN(Number(min)) && val < Number(min)) return false;
        if (max !== '' && !isNaN(Number(max)) && val > Number(max)) return false;
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
      if (col && (col.type === 'number' || col.type === 'currency' || col.type === 'fdv_million' || col.type === 'ratio')) {
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
                  style={{ cursor: 'pointer', textAlign: col.type === 'number' || col.type === 'currency' ? 'right' : 'left' }}
                >
                  {col.label}
                  {sortConfig.key === col.key ? (sortConfig.direction === 'asc' ? ' ▲' : ' ▼') : ''}
                  {(col.key === 'fees_30d_change' || col.key === 'revenue_30d_change') && (
                    <div className="change-sublabel">30d</div>
                  )}
                </th>
              ))}
            </tr>
            <tr>
              {columns.map((col) => (
                <th key={col.key} style={{ textAlign: col.type === 'number' || col.type === 'currency' ? 'right' : 'left' }}>
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
                        type="number"
                        value={filters[col.key].min}
                        onChange={(e) => handleFilterChange(col.key, e.target.value, 'min')}
                        placeholder="Min"
                        style={{ width: 50 }}
                      />
                      <input
                        type="number"
                        value={filters[col.key].max}
                        onChange={(e) => handleFilterChange(col.key, e.target.value, 'max')}
                        placeholder="Max"
                        style={{ width: 50 }}
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
                    style={{ textAlign: col.type === 'number' || col.type === 'currency' || col.type === 'fdv_million' || col.type === 'ratio' ? 'right' : 'left', whiteSpace: 'nowrap' }}
                  >
                    {col.key === 'fees_30d_change' || col.key === 'revenue_30d_change' ? (
                      formatPercentChange(row[col.key])
                    ) : col.type === 'fdv_million' && row[col.key] != null ? (
                      <span>
                        {formatCompactUSD(row[col.key])} <span className="usd-label">USD</span>
                      </span>
                    ) : col.type === 'currency' && row[col.key] != null ? (
                      <span>
                        {formatCompactUSD(row[col.key])} <span className="usd-label">USD</span>
                      </span>
                    ) : col.type === 'ratio' ? (
                      row[col.key] == null || isNaN(row[col.key]) ? '--' : `${Number(row[col.key]).toFixed(1)}x`
                    ) : row[col.key] != null ? (
                      row[col.key].toString()
                    ) : ''}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p style={{ marginTop: 8, fontSize: 12, color: '#888' }}>
        Click column headers to sort. Filter each column individually. Numeric columns support min/max.
      </p>
       <p style={{ marginTop: 4, fontSize: 12, color: '#888' }}>
        <strong>Note:</strong> Forward P/F and P/R ratios are calculated as <code>FDV / (30d Fees/Revenue * 12)</code>.
      </p>
    </div>
  );
}

function App() {
  const feesData = useTableData('fees_analysis.json');
  const revenueData = useTableData('revenue_analysis.json');
  const [activeTab, setActiveTab] = useState('fees');

  return (
    <div className="App">
      <h1>Protocol Fees/Revenue Screener</h1>
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
