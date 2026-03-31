import { useState } from 'react';
import { useTableData } from './hooks/useTableData';
import { Table } from './components/Table';
import { Sparkline } from './components/Sparkline';
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

function LoadingState() {
  return (
    <div className="loading-state">
      <div className="spinner" />
      <p>Loading protocol data...</p>
    </div>
  );
}

function ErrorState({ error, onRetry }) {
  return (
    <div className="error-state">
      <p className="error-title">Failed to load data</p>
      <p className="error-message">{error}</p>
      <button onClick={onRetry} className="retry-button">Retry</button>
    </div>
  );
}

// Extended table component with sparklines for top 50 by P/F or P/R ratio
function TableWithSparklines({ columns, data, dataType }) {
  // Get top 50 by ratio for sparklines
  const top50Slugs = [...data]
    .filter(row => row[dataType === 'fees' ? 'pf_ratio_forward_1y' : 'pr_ratio_forward_1y'] != null)
    .sort((a, b) => Number(a[dataType === 'fees' ? 'pf_ratio_forward_1y' : 'pr_ratio_forward_1y']) - Number(b[dataType === 'fees' ? 'pf_ratio_forward_1y' : 'pr_ratio_forward_1y']))
    .slice(0, 50)
    .map(row => row.slug)
    .filter(Boolean);

  const top50Set = new Set(top50Slugs);

  // Build sparkline data map - placeholder for now, will be populated with historical data
  const sparklines = {};

  return (
    <Table
      columns={columns}
      data={data}
      sparklines={sparklines}
    />
  );
}

function App() {
  const { data: feesData, loading: feesLoading, error: feesError, refetch: refetchFees } = useTableData('data/exports/fees_analysis.json');
  const { data: revenueData, loading: revenueLoading, error: revenueError, refetch: refetchRevenue } = useTableData('data/exports/revenue_analysis.json');
  const [activeTab, setActiveTab] = useState('fees');

  const totalProtocols = activeTab === 'fees' ? feesData.length : revenueData.length;
  const loading = activeTab === 'fees' ? feesLoading : revenueLoading;
  const error = activeTab === 'fees' ? feesError : revenueError;
  const refetch = activeTab === 'fees' ? refetchFees : refetchRevenue;

  return (
    <div className="App">
      <header className="app-header">
        <h1>Protocol Fees/Revenue Screener</h1>
        <div className="header-stats">
          <span className="stat-pill">{totalProtocols} protocols</span>
          <span className="update-badge">Weekly data</span>
        </div>
      </header>

      <div className="tabs">
        <button
          onClick={() => setActiveTab('fees')}
          className={activeTab === 'fees' ? 'active' : ''}
        >
          Fees
        </button>
        <button
          onClick={() => setActiveTab('revenue')}
          className={activeTab === 'revenue' ? 'active' : ''}
        >
          Revenue
        </button>
      </div>

      {loading && <LoadingState />}
      {error && <ErrorState error={error} onRetry={refetch} />}

      {!loading && !error && (
        <>
          {activeTab === 'fees' && (
            <TableWithSparklines
              columns={FEES_COLUMNS}
              data={feesData}
              dataType="fees"
            />
          )}
          {activeTab === 'revenue' && (
            <TableWithSparklines
              columns={REVENUE_COLUMNS}
              data={revenueData}
              dataType="revenue"
            />
          )}
        </>
      )}
    </div>
  );
}

export default App;
