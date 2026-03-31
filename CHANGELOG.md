# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.0.0] - 2026-04-01

### Added
- PWA support with vite-plugin-pwa, including service worker and offline caching
- Mobile-responsive design with dark mode support and touch-friendly interactions
- Modular component architecture (Table, Sparkline, TooltipPortal, useTableData hook)
- Vitest testing framework with 21 passing tests for formatters and data hooks
- Loading and error states for better UX during data fetching
- Interactive table with sorting, filtering, and sticky headers
- Sparkline chart visualization using recharts for top 50 protocols

### Changed
- Migrated from monolithic App.jsx to modular component structure
- Improved data fetching with 10-second timeout and AbortController
- Enhanced table sorting with proper NaN handling

### Fixed
- NaN sort comparator bug in Table component
- Array index anti-pattern for React keys (now using stable row identifiers)
- Removed dead code (unused tooltipRef)
