const BASE = import.meta.env.VITE_API_URL ?? ''

async function request(method, path, body = null) {
  const opts = {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
  }
  if (body) opts.body = JSON.stringify(body)

  let res
  try {
    res = await fetch(`${BASE}${path}`, opts)
  } catch {
    throw new Error('Servidor indisponível. Verifique se o backend está rodando.')
  }

  if (res.status === 204) return null

  const data = await res.json().catch(() => ({}))

  if (!res.ok) {
    const msg = Array.isArray(data?.detail)
      ? data.detail.map(e => e.msg || e).join(', ')
      : data?.detail || `Erro ${res.status}`
    throw new Error(msg)
  }

  return data
}

export const api = {
  get:  (path)       => request('GET',    path),
  post: (path, body) => request('POST',   path, body),
  put:  (path, body) => request('PUT',    path, body),
  del:  (path)       => request('DELETE', path),
}
