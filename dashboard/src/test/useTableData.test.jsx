import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { useTableData } from '../hooks/useTableData'

// Mock fetch globally
const mockFetch = vi.fn()
global.fetch = mockFetch

// Test component that uses the hook
function TestComponent({ url }) {
  const { data, loading, error } = useTableData(url)

  if (loading) return <div data-testid="loading">Loading...</div>
  if (error) return <div data-testid="error">{error}</div>
  return <div data-testid="data">{JSON.stringify(data)}</div>
}

describe('useTableData', () => {
  it('starts with loading state', () => {
    mockFetch.mockImplementationOnce(() => new Promise(() => { }))
    render(<TestComponent url="/test.json" />)
    expect(screen.getByTestId('loading')).toBeInTheDocument()
  })

  it('handles successful data fetch', async () => {
    const mockData = [{ id: 1, name: 'Test' }]
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    })

    render(<TestComponent url="/test.json" />)

    await waitFor(() => {
      expect(screen.getByTestId('data')).toHaveTextContent(JSON.stringify(mockData))
    })
  })

  it('handles fetch error', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
      statusText: 'Not Found',
    })

    render(<TestComponent url="/test.json" />)

    await waitFor(() => {
      expect(screen.getByTestId('error')).toHaveTextContent('HTTP 404: Not Found')
    })
  })

  it('handles network error', async () => {
    mockFetch.mockRejectedValueOnce(new Error('Network error'))

    render(<TestComponent url="/test.json" />)

    await waitFor(() => {
      expect(screen.getByTestId('error')).toHaveTextContent('Network error')
    })
  })
})
