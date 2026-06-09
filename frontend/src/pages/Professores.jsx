import { useState, useEffect } from 'react'
import { api } from '../api/client'
import { useToast } from '../components/Toast'
import Modal from '../components/Modal'
import { ConfirmDialog } from '../components/Modal'
import { Loading, ErrorBox } from '../components/StateBox'

const EMPTY = {
  nome: '', cpf: '', email: '', telefone: '',
  especialidade: '', ativo: true,
}

function PlusIcon() {
  return <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
}
function EditIcon() {
  return <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
}
function TrashIcon() {
  return <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/></svg>
}

export default function Professores() {
  const toast = useToast()
  const [professores, setProfessores] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [search, setSearch] = useState('')
  const [filterAtivo, setFilterAtivo] = useState('')

  const [modal, setModal] = useState({ open: false, mode: 'create', data: null })
  const [form, setForm] = useState(EMPTY)
  const [saving, setSaving] = useState(false)

  const [confirm, setConfirm] = useState({ open: false, data: null })
  const [deleting, setDeleting] = useState(false)

  async function load() {
    try {
      setLoading(true); setError(null)
      const data = await api.get('/professores')
      setProfessores(data)
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])

  const filtered = professores.filter(p => {
    const q = search.toLowerCase()
    const matchSearch = !q || p.nome.toLowerCase().includes(q) || p.especialidade.toLowerCase().includes(q)
    const matchAtivo = filterAtivo === '' || String(p.ativo) === filterAtivo
    return matchSearch && matchAtivo
  })

  const ativos = professores.filter(p => p.ativo).length
  const especialidades = [...new Set(professores.map(p => p.especialidade))].length

  function openCreate() { setForm(EMPTY); setModal({ open: true, mode: 'create', data: null }) }
  function openEdit(p)  { setForm({ ...p }); setModal({ open: true, mode: 'edit', data: p }) }

  async function save() {
    if (!form.nome || !form.cpf || !form.email || !form.telefone || !form.especialidade) {
      toast('Preencha todos os campos obrigatórios.', 'warning'); return
    }
    try {
      setSaving(true)
      if (modal.mode === 'create') {
        await api.post('/professores', form)
        toast('Professor cadastrado!')
      } else {
        await api.put(`/professores/${modal.data.id}`, {
          nome: form.nome, email: form.email,
          telefone: form.telefone, especialidade: form.especialidade, ativo: form.ativo,
        })
        toast('Professor atualizado!')
      }
      setModal({ open: false }); load()
    } catch (e) { toast(e.message, 'error') }
    finally { setSaving(false) }
  }

  async function del() {
    try {
      setDeleting(true)
      await api.del(`/professores/${confirm.data.id}`)
      toast('Professor excluído.')
      setConfirm({ open: false }); load()
    } catch (e) { toast(e.message, 'error') }
    finally { setDeleting(false) }
  }

  if (error) return <ErrorBox message={error} onRetry={load} />

  return (
    <>
      {/* Stats */}
      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-label">Total de Professores</div>
          <div className="stat-value">{professores.length}</div>
          <div className="stat-sub">cadastrados no sistema</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Ativos</div>
          <div className="stat-value" style={{ color: 'var(--success)' }}>{ativos}</div>
          <div className="stat-sub">{professores.length - ativos} inativo{professores.length - ativos !== 1 ? 's' : ''}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Especialidades</div>
          <div className="stat-value" style={{ color: 'var(--primary)' }}>{especialidades}</div>
          <div className="stat-sub">áreas distintas</div>
        </div>
      </div>

      {/* Tabela */}
      <div className="card">
        <div className="card-header">
          <div>
            <div className="card-title">Professores</div>
            <div className="card-count">{filtered.length} de {professores.length} registros</div>
          </div>
          <div className="card-actions">
            <button className="btn btn-primary" onClick={openCreate}><PlusIcon /> Novo Professor</button>
          </div>
        </div>

        <div className="filter-bar">
          <div className="search-wrap">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input className="search-input" placeholder="Buscar por nome ou especialidade..." value={search} onChange={e => setSearch(e.target.value)} />
          </div>
          <select className="filter-select" value={filterAtivo} onChange={e => setFilterAtivo(e.target.value)}>
            <option value="">Todos</option>
            <option value="true">Ativos</option>
            <option value="false">Inativos</option>
          </select>
        </div>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>Especialidade</th>
                <th>E-mail</th>
                <th>Telefone</th>
                <th>CPF</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            {loading ? <Loading rows={5} /> : (
              <tbody>
                {filtered.length === 0 ? (
                  <tr><td colSpan={7}>
                    <div className="state-box">
                      <p>Nenhum professor encontrado.</p>
                      <button className="btn btn-primary" onClick={openCreate}><PlusIcon /> Cadastrar Professor</button>
                    </div>
                  </td></tr>
                ) : filtered.map(p => (
                  <tr key={p.id}>
                    <td className="td-name">{p.nome}</td>
                    <td>{p.especialidade}</td>
                    <td style={{ fontSize: '13px', color: 'var(--text-2)' }}>{p.email}</td>
                    <td className="td-mono">{p.telefone}</td>
                    <td className="td-mono">{p.cpf}</td>
                    <td>
                      <span className={`badge ${p.ativo ? 'badge-success' : 'badge-danger'}`}>
                        {p.ativo ? 'Ativo' : 'Inativo'}
                      </span>
                    </td>
                    <td>
                      <div className="td-actions">
                        <button className="btn btn-ghost btn-sm" onClick={() => openEdit(p)}><EditIcon /></button>
                        <button className="btn btn-ghost btn-sm" style={{ color: 'var(--danger)' }} onClick={() => setConfirm({ open: true, data: p })}><TrashIcon /></button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            )}
          </table>
        </div>
      </div>

      {/* Modal */}
      <Modal
        open={modal.open}
        title={modal.mode === 'create' ? 'Novo Professor' : 'Editar Professor'}
        onClose={() => setModal({ open: false })}
        footer={<>
          <button className="btn btn-secondary" onClick={() => setModal({ open: false })}>Cancelar</button>
          <button className="btn btn-primary" onClick={save} disabled={saving}>{saving ? 'Salvando...' : 'Salvar'}</button>
        </>}
      >
        <div className="form-grid form-grid-2">
          <div className="form-field full">
            <label>Nome completo *</label>
            <input value={form.nome} onChange={e => setForm(f => ({ ...f, nome: e.target.value }))} placeholder="Ex: João da Silva" />
          </div>
          <div className="form-field">
            <label>CPF *</label>
            <input value={form.cpf} onChange={e => setForm(f => ({ ...f, cpf: e.target.value }))} placeholder="000.000.000-00" disabled={modal.mode === 'edit'} />
          </div>
          <div className="form-field">
            <label>Telefone *</label>
            <input value={form.telefone} onChange={e => setForm(f => ({ ...f, telefone: e.target.value }))} placeholder="(00) 90000-0000" />
          </div>
          <div className="form-field full">
            <label>E-mail *</label>
            <input type="email" value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} placeholder="professor@escola.com" />
          </div>
          <div className="form-field full">
            <label>Especialidade *</label>
            <input value={form.especialidade} onChange={e => setForm(f => ({ ...f, especialidade: e.target.value }))} placeholder="Ex: Matemática, Língua Portuguesa..." />
          </div>
          {modal.mode === 'edit' && (
            <div className="form-field full">
              <label className="checkbox-row">
                <input type="checkbox" checked={form.ativo} onChange={e => setForm(f => ({ ...f, ativo: e.target.checked }))} />
                <span>Professor ativo</span>
              </label>
            </div>
          )}
        </div>
      </Modal>

      <ConfirmDialog
        open={confirm.open}
        title="Excluir Professor"
        message={`Excluir "${confirm.data?.nome}"? Esta ação não pode ser desfeita.`}
        onConfirm={del}
        onCancel={() => setConfirm({ open: false })}
        loading={deleting}
      />
    </>
  )
}
