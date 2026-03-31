import { useEffect, useState, useCallback } from 'react';

export function useTableData(url) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    let cancelled = false;
    let timeoutId = null;

    try {
      setLoading(true);
      setError(null);

      // Add timeout to prevent hanging requests
      const controller = new AbortController();
      timeoutId = setTimeout(() => controller.abort(), 10000);

      const response = await fetch(url, { signal: controller.signal });
      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const json = await response.json();

      if (!cancelled) {
        setData(json);
      }
    } catch (err) {
      if (!cancelled) {
        if (err.name === 'AbortError') {
          setError('Request timed out after 10 seconds');
        } else {
          setError(err.message || 'Failed to load data');
        }
        console.error('Failed to load', url, err);
      }
    } finally {
      if (!cancelled) {
        setLoading(false);
      }
    }

    return () => {
      cancelled = true;
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, [url]);

  useEffect(() => {
    const cleanup = fetchData();
    return () => {
      if (typeof cleanup === 'function') cleanup();
    };
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}
