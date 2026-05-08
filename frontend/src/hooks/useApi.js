import { useState, useEffect } from 'react';

function getAuthHeaders() {
  const token = localStorage.getItem('token');
  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

function normalizeUrl(url) {
  return url.replace(/\/+$/, '');
}

export function useApi(url, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [total, setTotal] = useState(0);
  const [skip, setSkip] = useState(options.skip || 0);
  const limit = options.limit || 100;

  useEffect(() => {
    setLoading(true);
    const normalizedUrl = normalizeUrl(url);
    const urlObj = new URL(normalizedUrl, window.location.origin);
    urlObj.searchParams.set('skip', skip);
    urlObj.searchParams.set('limit', limit);
    fetch(urlObj.toString(), {
      headers: getAuthHeaders()
    })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(json => {
        setData(json.data);
        setTotal(json.total);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [url, skip, limit]);

  return { data, loading, error, total, skip, limit, setSkip };
}

export { getAuthHeaders };