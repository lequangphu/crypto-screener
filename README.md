# Crypto Protocol Valuation Screener

A full-stack web application for analyzing cryptocurrency protocol valuations and identifying potentially undervalued investment opportunities based on key financial metrics.

## 🚀 Live Demo

[View the live application](https://lequangphu.github.io/crypto-screener/)

## ✨ Features

- **Real-time Data Analysis**: Processes 5000+ cryptocurrency protocols from DeFiLlama and CoinMarketCap APIs
- **Financial Metrics**: Calculates P/F (Price-to-Fees) and P/R (Price-to-Revenue) ratios for valuation analysis
- **Interactive Dashboard**: Sortable and filterable data tables with responsive design
- **Advanced Filtering**: Filter by protocol name, category, market cap, and financial metrics
- **Data Export**: Export analysis results as JSON for further analysis
- **Mobile Responsive**: Optimized for desktop and mobile devices
- **Tooltip System**: Interactive help system with detailed metric explanations

## 🏗️ Architecture

### Backend (ETL Pipeline)
- **Data Ingestion**: Python scripts fetching data from multiple APIs
- **Database**: DuckDB for high-performance analytical queries
- **Data Processing**: Pandas for data manipulation and transformation
- **Error Handling**: Robust retry logic and comprehensive logging

### Frontend (Dashboard)
- **Framework**: React 19 with modern hooks
- **Build Tool**: Vite for fast development and optimized builds
- **Styling**: Custom CSS with responsive design
- **Deployment**: GitHub Pages for zero-cost hosting

## 🛠️ Tech Stack

### Backend
- **Python 3.13+** - Core backend development
- **DuckDB** - Analytical database
- **Pandas** - Data manipulation
- **Requests** - HTTP API client
- **UV** - Modern Python package management

### Frontend
- **React 19** - UI framework
- **Vite** - Build tool and dev server
- **ESLint** - Code quality
- **CSS3** - Styling and animations

### APIs
- **DeFiLlama API** - Protocol data, fees, and revenue
- **CoinMarketCap API** - Market cap and pricing data

## 📋 Prerequisites

- Python 3.13 or higher
- Node.js 18 or higher
- UV package manager
- CoinMarketCap API key (optional, for enhanced data)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/crypto-screener.git
cd crypto-screener
```

### 2. Backend Setup
```bash
# Install Python dependencies
uv sync

# Set up environment variables (optional)
cp .env.example .env
# Edit .env and add your CoinMarketCap API key
```

### 3. Run Data Pipeline
```bash
# Ingest data from APIs
uv run ingest_data.py

# Transform and enrich data
uv run transform_data.py

# Analyze and export data for dashboard
uv run analyze_protocols.py
```

### 4. Frontend Setup
```bash
cd dashboard

# Install dependencies
npm install

# Copy data files to public directory
npm run copy-data

# Start development server
npm run dev
```

### 5. Build for Production
```bash
# Build the dashboard
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
crypto-screener/
├── data/
│   ├── crypto.duckdb          # DuckDB database file
│   └── exports/               # JSON exports for dashboard
│       ├── fees_analysis.json
│       └── revenue_analysis.json
├── dashboard/                 # React frontend
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── App.css           # Styling
│   │   └── main.jsx          # Entry point
│   ├── public/               # Static assets
│   ├── package.json          # Frontend dependencies
│   └── vite.config.js        # Vite configuration
├── docs/                     # Documentation
│   ├── prd.md               # Product Requirements Document
│   ├── architecture.md      # System architecture
│   └── etl_dashboard_plan.md # Implementation plan
├── ingest_data.py           # Data ingestion script
├── transform_data.py        # Data transformation script
├── analyze_protocols.py     # Analysis and export script
├── pyproject.toml          # Python dependencies
└── README.md               # This file
```

## 📊 Key Metrics Explained

### P/F Ratio (Price-to-Fees)
- **Formula**: `FDV / (30d Fees × 12)`
- **Purpose**: Measures how expensive a protocol is relative to its fee generation
- **Lower is better**: Indicates potentially undervalued protocols

### P/R Ratio (Price-to-Revenue)
- **Formula**: `FDV / (30d Revenue × 12)`
- **Purpose**: Measures how expensive a protocol is relative to its revenue
- **Lower is better**: Indicates potentially undervalued protocols

### FDV (Fully Diluted Valuation)
- **Definition**: Total market cap if all tokens were in circulation
- **Source**: CoinMarketCap API
- **Usage**: Used as the "price" component in valuation ratios

## 🔧 Development

### Running the Complete Pipeline
```bash
# Run all ETL steps in sequence
uv run ingest_data.py && uv run transform_data.py && uv run analyze_protocols.py

# Copy data to dashboard and start dev server
cd dashboard && npm run etl-and-copy && npm run dev
```

### Data Pipeline Overview
1. **Ingestion** (`ingest_data.py`): Fetches data from APIs and loads into DuckDB
2. **Transformation** (`transform_data.py`): Joins and enriches data with market cap info
3. **Analysis** (`analyze_protocols.py`): Calculates metrics and exports JSON for dashboard

### Frontend Development
```bash
cd dashboard
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
npm run preview      # Preview production build
```

## 🚀 Deployment

### GitHub Pages
The application is automatically deployed to GitHub Pages when you push to the main branch.

### Manual Deployment
```bash
# Build the dashboard
cd dashboard
npm run build

# The built files are in dashboard/dist/
# Copy these to your web server
```

## 📈 Data Sources

### DeFiLlama API
- **Protocols**: Basic protocol information and metadata
- **Fees**: Daily fee data for all protocols
- **Revenue**: Daily revenue data for all protocols
- **Rate Limit**: 100 requests per minute
- **Authentication**: None required

### CoinMarketCap API
- **Market Data**: Current market cap, FDV, and pricing
- **Rate Limit**: Varies by plan
- **Authentication**: API key required
- **Usage**: Enriches protocol data with market valuation

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Ensure DuckDB file exists
   ls -la data/crypto.duckdb
   
   # Recreate if missing
   uv run ingest_data.py
   ```

2. **API Rate Limiting**
   - DeFiLlama: Wait 1 minute between requests
   - CoinMarketCap: Check your API key and plan limits

3. **Frontend Data Loading Issues**
   ```bash
   # Ensure data files exist
   ls -la data/exports/
   
   # Regenerate if missing
   uv run analyze_protocols.py
   cd dashboard && npm run copy-data
   ```

4. **Build Errors**
   ```bash
   # Clear node modules and reinstall
   cd dashboard
   rm -rf node_modules package-lock.json
   npm install
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [DeFiLlama](https://defillama.com/) for providing comprehensive DeFi data
- [CoinMarketCap](https://coinmarketcap.com/) for market data
- [DuckDB](https://duckdb.org/) for high-performance analytics
- [React](https://reactjs.org/) and [Vite](https://vitejs.dev/) for the frontend framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Review the [documentation](docs/)
3. Open an [issue](https://github.com/your-username/crypto-screener/issues)

---

**Built with ❤️ for the crypto community**