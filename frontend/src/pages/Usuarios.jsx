import { useState, useEffect } from 'react'
import { api } from '../api/client'
import { useToast } from '../components/Toast'
import Modal from '../components/Modal'
import { ConfirmDialog } from '../components/Modal'
import { Loading, Empty, ErrorBox, Badge } from '../components/StateBox'

const EMPTY = { nome: '', email: '', senha: '', ativo: true, perfil_id: '' }

function PlusIcon() {
  return <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
}

export default function Usuarios() {
  const toast = useToast()
  const [usuarios, setUsuarios] = useState([])
  const [perfis, setPerfis] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [search, setSearch] = useState('')

  const [modal, setModal] = useState({ open: false, mode: 'create', data: null })
  const [form, setForm] = useState(EMPTY)
  const [saving, setSaving] = useState(false)

  const [confirm, setConfirm] = useState({ open: false, data: null })
  const [deleting, setDeleting] = useState(false)

  async function load() {
    try {
      setLoading(true); setError(null)
      const [u, p] = await Promise.all([api.get('/usuarios'), api.get('/perfis')])
      setUsuarios(u); setPerfis(p)
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])

  function getPerfil(id) { return perfis.find(p => p.id === id) }

  const filtered = usuarios.filter(u => {
    const q = search.toLowerCase()
    return !q || u.nome.toLowerCase().includes(q) || u.email.toLowerCase().includes(q)
  })

  function openCreate() { setForm({ ...EMPTY, perfil_id: perfis[0]?.id || '' }); setModal({ open: true, mode: 'create', data: null }) }
  function openEdit(u) {
    setForm({ nome: u.nome, email: u.email, senha: '', ativo: u.ativo, perfil_id: String(u.perfil_id) })
    setModal({ open: true, mode: 'edit', data: u })
  }

  async function handleSave() {
    if (!form.nome || !form.email || !form.perfil_id) { toast('Preencha os campos obrigatórios.', 'warning'); return }
    if (modal.mode === 'create' && form.senha.length < 8) { toast('A senha deve ter no mínimo 8 caracteres.', 'warning'); return }
    try {
      setSaving(true)
      const payload = { ...form, perfil_id: Number(form.perfil_id) }
      if (modal.mode === 'create') {
        await api.post('/usuarios', payload); toast('Usuário criado!')
      } else {
        const { senha, ...upd } = payload
        await api.put(`/usuarios/${modal.data.id}`, upd); toast('Usuário atualizado!')
      }
      setModal({ open: false }); load()
    } catch (e) { toast(e.message, 'error') }
    finally { setSaving(false) }
  }

  async function handleDelete() {
    try {
      setDeleting(true)
      await api.del(`/usuarios/${confirm.data.id}`)
      toast('Usuário excluído.'); setConfirm({ open: false }); load()
    } catch (e) { toast(e.message, 'error') }
    finally { setDeleting(false) }
  }

  if (error) return <ErrorBox message={error} onRetry={load} />

  return (
    <>
      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-label">Total de Usuários</div>
          <div className="stat-value">{usuarios.length}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Ativos</div>
          <div className="stat-value" style={{ color: 'var(--success)' }}>{usuarios.filter(u => u.ativo).length}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Perfis</div>
          <div className="stat-value" style={{ color: 'var(--primary)' }}>{perfis.length}</div>
          <div className="stat-sub">tipos de acesso</div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div>
            <div className="card-title">Usuários do Sistema</div>
            <div className="card-count">{filtered.length} de {usuarios.length} usuários</div>
          </div>
          <div className="card-actions">
            <button className="btn btn-primary" onClick={openCreate}><PlusIcon /> Novo Usuário</button>
          </div>
        </div>

        <div className="filter-bar">
          <div className="search-wrap">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input className="search-input" placeholder="Buscar por nome ou e-mail..." value={search} onChange={e => setSearch(e.target.value)} />
          </div>
        </div>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>E-mail</th>
                <th>Perfil</th>
                <th>Cadastro</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            {loading ? <Loading rows={4} /> : filtered.length === 0 ? (
              <tbody><tr><td colSpan={6}>
                <Empty
                  title="Nenhum usuário encontrado"
                  action={<button className="btn btn-primary" onClick={openCreate}><PlusIcon /> Criar Usuário</button>}
                />
              </td></tr></tbody>
            ) : (
              <tbody>
                {filtered.map(u => {
                  const perfil = getPerfil(u.perfil_id)
                  return (
                    <tr key={u.id}>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                          <div style={{
                            width: '30px', height: '30px', borderRadius: '50%',
                            background: 'var(--primary-light)',
                            color: 'var(--primary)',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            fontWeight: 700, fontSize: '12px', flexShrink: 0,
                          }}>
                            {u.nome.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()}
                          </div>
                          <span className="td-name">{u.nome}</span>
                        </div>
                      </td>
                      <td className="td-mono" style={{ fontSize: '13px' }}>{u.email}</td>
                      <td>
                        {perfil
                          ? <span className="badge badge-info">{perfil.nome}</span>
                          : <span style={{ color: 'var(--text-3)' }}>—</span>
                        }
                      </td>
                      <td className="td-mono">{u.criado_em}</td>
                      <td><Badge status={u.ativo} /></td>
                      <td>
                        <div className="td-actions">
                          <button className="btn btn-ghost btn-sm" onClick={() => openEdit(u)}>
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                            </svg>
                          </button>
                          <button className="btn btn-ghost btn-sm" style={{ color: 'var(--danger)' }}
                            onClick={() => setConfirm({ open: true, data: u })}>
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                              <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                            </svg>
                          </button>
                        </div>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            )}
          </table>
        </div>
      </div>

      <Modal open={modal.open} title={modal.mode === 'create' ? 'Novo Usuário' : 'Editar Usuário'}
        onClose={() => setModal({ open: false })}
        footer={<>
          <button className="btn btn-secondary" onClick={() => setModal({ open: false })}>Cancelar</button>
          <button className="btn btn-primary" onClick={handleSave} disabled={saving}>{saving ? 'Salvando...' : 'Salvar'}</button>
        </>}
      >
        <div className="form-grid form-grid-2">
          <div className="form-field full">
            <label>Nome *</label>
            <input value={form.nome} onChange={e => setForm(f => ({ ...f, nome: e.target.value }))} placeholder="Nome completo" />
          </div>
          <div className="form-field full">
            <label>E-mail *</label>
            <input type="email" value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} placeholder="email@escola.com" />
          </div>
          {modal.mode === 'create' && (
            <div className="form-field full">
              <label>Senha * (mín. 8 caracteres)</label>
              <input type="password" value={form.senha} onChange={e => setForm(f => ({ ...f, senha: e.target.value }))} placeholder="••••••••" />
            </div>
          )}
          <div className="form-field">
            <label>Perfil de Acesso *</label>
            <select value={form.perfil_id} onChange={e => setForm(f => ({ ...f, perfil_id: e.target.value }))}>
              <option value="">Selecione o perfil</option>
              {perfis.map(p => <option key={p.id} value={p.id}>{p.nome}</option>)}
            </select>
          </div>
          <div className="form-field" style={{ justifyContent: 'flex-end' }}>
            <label className="checkbox-row">
              <input type="checkbox" checked={form.ativo} onChange={e => setForm(f => ({ ...f, ativo: e.target.checked }))} />
              <span>Usuário Ativo</span>
            </label>
          </div>
        </div>
      </Modal>

      <ConfirmDialog open={confirm.open} title="Excluir Usuário"
        message={`Excluir "${confirm.data?.nome}"?`}
        onConfirm={handleDelete} onCancel={() => setConfirm({ open: false })} loading={deleting} />
    </>
  )
}
