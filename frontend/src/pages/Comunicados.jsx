import { useState, useEffect } from 'react'
import { api } from '../api/client'
import { useToast } from '../components/Toast'
import Modal from '../components/Modal'
import { ConfirmDialog } from '../components/Modal'
import { ErrorBox } from '../components/StateBox'

const EMPTY = { titulo: '', conteudo: '', ativo: true, destinatario_id: '' }

function PlusIcon() {
  return <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
}

export default function Comunicados() {
  const toast = useToast()
  const [comunicados, setComunicados] = useState([])
  const [usuarios, setUsuarios] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [search, setSearch] = useState('')
  const [filterStatus, setFilterStatus] = useState('')

  const [modal, setModal] = useState({ open: false, mode: 'create', data: null })
  const [form, setForm] = useState(EMPTY)
  const [saving, setSaving] = useState(false)
  const [confirm, setConfirm] = useState({ open: false, id: null })
  const [deleting, setDeleting] = useState(false)

  async function load() {
    try {
      setLoading(true); setError(null)
      const [c, u] = await Promise.all([api.get('/comunicados'), api.get('/usuarios')])
      setComunicados(c); setUsuarios(u)
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])

  function getUser(id) { return usuarios.find(u => u.id === id) }

  const filtered = comunicados.filter(c => {
    const q = search.toLowerCase()
    const matchSearch = !q || c.titulo.toLowerCase().includes(q) || c.conteudo.toLowerCase().includes(q)
    const matchStatus = !filterStatus ||
      (filterStatus === 'ativo' && c.ativo) ||
      (filterStatus === 'inativo' && !c.ativo)
    return matchSearch && matchStatus
  }).sort((a, b) => b.id - a.id)

  function openCreate() { setForm({ ...EMPTY, destinatario_id: usuarios[0]?.id || '' }); setModal({ open: true, mode: 'create', data: null }) }
  function openEdit(c) {
    setForm({ titulo: c.titulo, conteudo: c.conteudo, ativo: c.ativo, destinatario_id: String(c.destinatario_id) })
    setModal({ open: true, mode: 'edit', data: c })
  }

  async function handleSave() {
    if (!form.titulo || !form.conteudo || !form.destinatario_id) {
      toast('Preencha todos os campos obrigatórios.', 'warning'); return
    }
    try {
      setSaving(true)
      const payload = { ...form, destinatario_id: Number(form.destinatario_id) }
      if (modal.mode === 'create') { await api.post('/comunicados', payload); toast('Comunicado enviado!') }
      else { await api.put(`/comunicados/${modal.data.id}`, payload); toast('Comunicado atualizado!') }
      setModal({ open: false }); load()
    } catch (e) { toast(e.message, 'error') }
    finally { setSaving(false) }
  }

  async function handleDelete() {
    try {
      setDeleting(true)
      await api.del(`/comunicados/${confirm.id}`)
      toast('Comunicado excluído.'); setConfirm({ open: false }); load()
    } catch (e) { toast(e.message, 'error') }
    finally { setDeleting(false) }
  }

  function dateLabel(d) {
    if (!d) return ''
    const [y, m, day] = d.split('-')
    return `${day}/${m}/${y}`
  }

  if (error) return <ErrorBox message={error} onRetry={load} />

  return (
    <>
      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-label">Total de Comunicados</div>
          <div className="stat-value">{comunicados.length}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Ativos</div>
          <div className="stat-value" style={{ color: 'var(--success)' }}>{comunicados.filter(c => c.ativo).length}</div>
          <div className="stat-sub">em exibição</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Inativos</div>
          <div className="stat-value" style={{ color: 'var(--text-3)' }}>{comunicados.filter(c => !c.ativo).length}</div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div>
            <div className="card-title">Comunicados</div>
            <div className="card-count">{filtered.length} de {comunicados.length} exibidos</div>
          </div>
          <div className="card-actions">
            <button className="btn btn-primary" onClick={openCreate}><PlusIcon /> Novo Comunicado</button>
          </div>
        </div>

        <div className="filter-bar">
          <div className="search-wrap">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input className="search-input" placeholder="Buscar por título ou conteúdo..." value={search} onChange={e => setSearch(e.target.value)} />
          </div>
          <select className="filter-select" value={filterStatus} onChange={e => setFilterStatus(e.target.value)}>
            <option value="">Todos os status</option>
            <option value="ativo">Ativo</option>
            <option value="inativo">Inativo</option>
          </select>
        </div>

        <div style={{ padding: '16px' }}>
          {loading ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {[1,2,3].map(i => <div key={i} className="skeleton" style={{ height: '100px', borderRadius: '10px' }} />)}
            </div>
          ) : filtered.length === 0 ? (
            <div className="state-box">
              <p>Nenhum comunicado encontrado.</p>
              <button className="btn btn-primary" onClick={openCreate}><PlusIcon /> Criar Comunicado</button>
            </div>
          ) : (
            <div className="comunicados-list">
              {filtered.map(c => {
                const dest = getUser(c.destinatario_id)
                return (
                  <div key={c.id} className={`comunicado-card ${c.ativo ? 'active-com' : 'inactive-com'}`}>
                    <div className="comunicado-header">
                      <div className="comunicado-title">{c.titulo}</div>
                      <div className="comunicado-actions">
                        <span className={`badge ${c.ativo ? 'badge-success' : 'badge-neutral'}`}>
                          {c.ativo ? 'Ativo' : 'Inativo'}
                        </span>
                        <button className="btn btn-ghost btn-sm" onClick={() => openEdit(c)}>
                          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                          </svg>
                        </button>
                        <button className="btn btn-ghost btn-sm" style={{ color: 'var(--danger)' }} onClick={() => setConfirm({ open: true, id: c.id })}>
                          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                          </svg>
                        </button>
                      </div>
                    </div>
                    <div className="comunicado-body">{c.conteudo}</div>
                    <div className="comunicado-meta">
                      <span>
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                        {dateLabel(c.enviado_em)}
                      </span>
                      <span>
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                        {dest ? dest.nome : `Usuário #${c.destinatario_id}`}
                      </span>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>

      <Modal open={modal.open} title={modal.mode === 'create' ? 'Novo Comunicado' : 'Editar Comunicado'}
        onClose={() => setModal({ open: false })}
        footer={<>
          <button className="btn btn-secondary" onClick={() => setModal({ open: false })}>Cancelar</button>
          <button className="btn btn-primary" onClick={handleSave} disabled={saving}>{saving ? 'Salvando...' : modal.mode === 'create' ? 'Enviar' : 'Salvar'}</button>
        </>}
      >
        <div className="form-grid">
          <div className="form-field">
            <label>Título *</label>
            <input value={form.titulo} onChange={e => setForm(f => ({ ...f, titulo: e.target.value }))} placeholder="Título do comunicado" />
          </div>
          <div className="form-field">
            <label>Destinatário *</label>
            <select value={form.destinatario_id} onChange={e => setForm(f => ({ ...f, destinatario_id: e.target.value }))}>
              <option value="">Selecione o destinatário</option>
              {usuarios.map(u => <option key={u.id} value={u.id}>{u.nome}</option>)}
            </select>
          </div>
          <div className="form-field">
            <label>Conteúdo *</label>
            <textarea value={form.conteudo} onChange={e => setForm(f => ({ ...f, conteudo: e.target.value }))} placeholder="Texto do comunicado..." style={{ minHeight: '100px' }} />
          </div>
          <div className="form-field">
            <label className="checkbox-row">
              <input type="checkbox" checked={form.ativo} onChange={e => setForm(f => ({ ...f, ativo: e.target.checked }))} />
              <span>Comunicado Ativo</span>
            </label>
          </div>
        </div>
      </Modal>

      <ConfirmDialog open={confirm.open} title="Excluir Comunicado"
        message="Deseja excluir este comunicado permanentemente?"
        onConfirm={handleDelete} onCancel={() => setConfirm({ open: false })} loading={deleting} />
    </>
  )
}
