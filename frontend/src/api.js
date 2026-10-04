const BASE = (import.meta.env.VITE_API_URL || '').replace(/\/+$/, '')
const CLIENT_KEY = 'aiEnglishCoachClientId'

function readDetail(data) {
  if (!data || data.detail == null) return ''
  if (typeof data.detail === 'string') return data.detail
  return 'Some of the data sent to the server was not valid.'
}

async function request(path, { method = 'GET', body, signal } = {}) {
  let response
  try {
    response = await fetch(`${BASE}${path}`, {
      method,
      headers: body ? { 'Content-Type': 'application/json' } : undefined,
      body: body ? JSON.stringify(body) : undefined,
      signal,
    })
  } catch (error) {
    if (error.name === 'AbortError') throw error
    throw new Error(
      'Cannot reach the backend. Make sure it is running (see the README).',
      { cause: error },
    )
  }

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    throw new Error(readDetail(data) || `Request failed (${response.status}).`)
  }
  return data
}

/** Anonymous id so progress can be stored without a login. */
export function getClientId() {
  try {
    const saved = localStorage.getItem(CLIENT_KEY)
    if (saved) return saved
  } catch {
    // storage unavailable: fall through and use a temporary id
  }

  const id =
    typeof crypto !== 'undefined' && crypto.randomUUID
      ? crypto.randomUUID()
      : `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 12)}`

  try {
    localStorage.setItem(CLIENT_KEY, id)
  } catch {
    // ignore
  }
  return id
}

export function generateExercise({ area, level, signal }) {
  return request('/api/generate-exercise', {
    method: 'POST',
    body: { area, level },
    signal,
  })
}

export function evaluateWriting({ level, topic, instructions, answer }) {
  return request('/api/evaluate-writing', {
    method: 'POST',
    body: { level, topic, instructions, answer },
  })
}

export function saveProgress({ clientId, area, level, score, total }) {
  return request('/api/progress', {
    method: 'POST',
    body: { client_id: clientId, area, level, score, total },
  })
}

export function getProgress(clientId, signal) {
  return request(`/api/progress?client_id=${encodeURIComponent(clientId)}`, {
    signal,
  })
}
