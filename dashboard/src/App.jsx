import { useEffect, useState } from 'react';
import './App.css';

// Column configs for renaming and type
const FEES_COLUMNS = [
  { key: 'protocol_name', label: 'Protocol', type: 'text' },
  { key: 'category', label: 'Category', type: 'text' },
  { key: 'fully_diluted_market_cap', label: 'FDV ($M)', type: 'fdv_million' },
  { key: 'fees_30d', label: 'Fees (30d) ($)', type: 'currency' },
  { key: 'fees_30d_change', label: 'Fees 30d Change (%)', type: 'number' },
  { key: 'pf_ratio_forward_1y', label: 'P/F Ratio (Forward 1y)', type: 'ratio' },
];
const REVENUE_COLUMNS = [
  { key: 'protocol_name', label: 'Protocol', type: 'text' },
  { key: 'category', label: 'Category', type: 'text' },
  { key: 'fully_diluted_market_cap', label: 'FDV ($M)', type: 'fdv_million' },
  { key: 'revenue_30d', label: 'Revenue (30d) ($)', type: 'currency' },
  { key: 'revenue_30d_change', label: 'Revenue 30d Change (%)', type: 'number' },
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

function Table({ columns, data, title }) {
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
      <h2>{title}</h2>
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
                    {col.type === 'fdv_million' && row[col.key] != null
                      ? Number(row[col.key] / 1_000_000).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
                      : col.type === 'currency' && row[col.key] != null
                        ? Number(row[col.key]).toLocaleString(undefined, { style: 'decimal', maximumFractionDigits: 2 })
                        : col.type === 'ratio' && row[col.key] != null
                          ? Number(row[col.key]).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
                          : row[col.key] != null
                            ? row[col.key].toString()
                            : ''}
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
  const feesData = useTableData('/fees_analysis.json');
  const revenueData = useTableData('/revenue_analysis.json');

  return (
    <div className="App">
      <h1>Protocol Analysis Dashboard</h1>
      <Table columns={FEES_COLUMNS} data={feesData} title="Fees Analysis" />
      <Table columns={REVENUE_COLUMNS} data={revenueData} title="Revenue Analysis" />
    </div>
  );
}

export default App;
