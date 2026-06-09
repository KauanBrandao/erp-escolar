import { useState } from 'react'
import { api, setToken } from '../api/client'

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!email || !senha) { setError('Preencha email e senha.'); return }
    try {
      setLoading(true); setError(null)
      const data = await api.post('/auth/login', { email, senha })
      setToken(data.access_token)
      onLogin()
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center',
      justifyContent: 'center', background: 'var(--bg)',
    }}>
      <div style={{
        background: 'var(--surface)', borderRadius: 'var(--r-lg)',
        border: '1px solid var(--border)', padding: '40px',
        width: '100%', maxWidth: '400px', boxShadow: 'var(--shadow-md)',
      }}>
        <div style={{ marginBottom: '28px', textAlign: 'center' }}>
          <div style={{
            width: '48px', height: '48px', borderRadius: '12px',
            background: 'var(--primary)', color: '#fff',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '22px', fontWeight: 700, margin: '0 auto 12px',
          }}>E</div>
          <h1 style={{ fontSize: '20px', fontWeight: 700, color: 'var(--text)', marginBottom: '4px' }}>
            ERP Escolar
          </h1>
          <p style={{ color: 'var(--text-2)', fontSize: '14px' }}>
            Faça login para continuar
          </p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div className="form-field">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="seu@email.com"
              autoFocus
            />
          </div>
          <div className="form-field">
            <label>Senha</label>
            <input
              type="password"
              value={senha}
              onChange={e => setSenha(e.target.value)}
              placeholder="••••••••"
            />
          </div>
          {error && (
            <div style={{
              background: 'var(--danger-bg)', border: '1px solid var(--danger-border)',
              borderRadius: 'var(--r-sm)', padding: '10px 12px',
              color: 'var(--danger)', fontSize: '13px',
            }}>{error}</div>
          )}
          <button className="btn btn-primary" type="submit" disabled={loading} style={{ marginTop: '4px' }}>
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
      </div>
    </div>
  )
}
