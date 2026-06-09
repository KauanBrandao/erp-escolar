import { useState, useEffect } from 'react'
import { api } from '../api/client'
import { useToast } from '../components/Toast'
import Modal from '../components/Modal'
import { ConfirmDialog } from '../components/Modal'
import { Loading, Empty, ErrorBox, Badge } from '../components/StateBox'

const EMPTY_FORM = {
  nome: '', cpf: '', telefone: '', matricula_numero: '',
  data_nascimento: '', ativo: true,
}

const EMPTY_MAT = { aluno_id: '', turma_id: '', data_matricula: '', status: 'ativa', observacao: '', valor_mensalidade: '' }

function PlusIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
    </svg>
  )
}
function EditIcon() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
    </svg>
  )
}
function TrashIcon() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="3 6 5 6 21 6"/>
      <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
      <path d="M10 11v6"/><path d="M14 11v6"/>
      <path d="M9 6V4h6v2"/>
    </svg>
  )
}

export default function Alunos() {
  const toast = useToast()
  const [alunos, setAlunos] = useState([])
  const [turmas, setTurmas] = useState([])
  const [matriculas, setMatriculas] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [search, setSearch] = useState('')
  const [filterStatus, setFilterStatus] = useState('')

  // modal aluno
  const [modal, setModal] = useState({ open: false, mode: 'create', data: null })
  const [form, setForm] = useState(EMPTY_FORM)
  const [saving, setSaving] = useState(false)

  // modal matrícula
  const [matModal, setMatModal] = useState({ open: false, data: null })
  const [matForm, setMatForm] = useState(EMPTY_MAT)
  const [savingMat, setSavingMat] = useState(false)

  // confirm
  const [confirm, setConfirm] = useState({ open: false, id: null, nome: '' })
  const [deleting, setDeleting] = useState(false)

  async function load() {
    try {
      setLoading(true); setError(null)
      const [a, t, m] = await Promise.all([
        api.get('/alunos'),
        api.get('/turmas'),
        api.get('/matriculas'),
      ])
      setAlunos(a); setTurmas(t); setMatriculas(m)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  function getMatricula(alunoId) {
    return matriculas.find(m => m.aluno_id === alunoId)
  }
  function getTurmaName(turmaId) {
    return turmas.find(t => t.id === turmaId)?.nome || '—'
  }

  const filtered = alunos.filter(a => {
    const q = search.toLowerCase()
    const mat = getMatricula(a.id)
    const matchSearch = !q || a.nome.toLowerCase().includes(q) ||
      a.cpf?.includes(q) || String(a.matricula_numero).includes(q)
    const matchStatus = !filterStatus || mat?.status === filterStatus
    return matchSearch && matchStatus
  })

  // ---- ALUNO CRUD ----
  function openCreate() {
    setForm(EMPTY_FORM)
    setModal({ open: true, mode: 'create', data: null })
  }
  function openEdit(aluno) {
    setForm({ ...aluno, matricula_numero: String(aluno.matricula_numero) })
    setModal({ open: true, mode: 'edit', data: aluno })
  }

  async function handleSave() {
    if (!form.nome || !form.cpf || !form.telefone || !form.matricula_numero || !form.data_nascimento) {
      toast('Preencha todos os campos obrigatórios.', 'warning'); return
    }
    try {
      setSaving(true)
      const payload = { ...form, matricula_numero: Number(form.matricula_numero) }
      if (modal.mode === 'create') {
        await api.post('/alunos', payload)
        toast('Aluno cadastrado com sucesso!')
      } else {
        const { cpf, matricula_numero, data_nascimento, ...upd } = payload
        await api.put(`/alunos/${modal.data.id}`, upd)
        toast('Aluno atualizado com sucesso!')
      }
      setModal({ open: false })
      load()
    } catch (e) {
      toast(e.message, 'error')
    } finally {
      setSaving(false)
    }
  }

  function confirmDelete(aluno) {
    setConfirm({ open: true, id: aluno.id, nome: aluno.nome })
  }
  async function handleDelete() {
    try {
      setDeleting(true)
      await api.del(`/alunos/${confirm.id}`)
      toast('Aluno excluído.')
      setConfirm({ open: false })
      load()
    } catch (e) {
      toast(e.message, 'error')
    } finally {
      setDeleting(false)
    }
  }

  // ---- MATRÍCULA ----
  function openMatricula(aluno) {
    const mat = getMatricula(aluno.id)
    if (mat) {
      setMatForm({ ...mat, turma_id: String(mat.turma_id) })
      setMatModal({ open: true, data: mat, alunoId: aluno.id })
    } else {
      setMatForm({ ...EMPTY_MAT, aluno_id: aluno.id, data_matricula: new Date().toISOString().slice(0, 10) })
      setMatModal({ open: true, data: null, alunoId: aluno.id })
    }
  }

  async function handleSaveMatricula() {
    try {
      setSavingMat(true)
      const payload = {
        ...matForm,
        turma_id: Number(matForm.turma_id),
        aluno_id: Number(matModal.alunoId),
        valor_mensalidade: matForm.valor_mensalidade ? Number(matForm.valor_mensalidade) : 0,
      }
      if (matModal.data) {
        const { aluno_id, data_matricula, valor_mensalidade, ...upd } = payload
        await api.put(`/matriculas/${matModal.data.id}`, upd)
        toast('Matrícula atualizada!')
      } else {
        await api.post('/matriculas', payload)
        toast('Matrícula criada! 12 mensalidades geradas automaticamente.')
      }
      setMatModal({ open: false })
      load()
    } catch (e) {
      toast(e.message, 'error')
    } finally {
      setSavingMat(false)
    }
  }

  const totalAtivos = alunos.filter(a => a.ativo).length

  return (
    <>
      {/* Stats */}
      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-label">Total de Alunos</div>
          <div className="stat-value">{alunos.length}</div>
          <div className="stat-sub">cadastrados no sistema</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Ativos</div>
          <div className="stat-value" style={{ color: 'var(--success)' }}>{totalAtivos}</div>
          <div className="stat-sub">{alunos.length ? Math.round(totalAtivos / alunos.length * 100) : 0}% do total</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Matrículas Ativas</div>
          <div className="stat-value" style={{ color: 'var(--primary)' }}>
            {matriculas.filter(m => m.status === 'ativa').length}
          </div>
          <div className="stat-sub">em turmas regulares</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Trancadas</div>
          <div className="stat-value" style={{ color: 'var(--warning)' }}>
            {matriculas.filter(m => m.status === 'trancada').length}
          </div>
          <div className="stat-sub">aguardando reativação</div>
        </div>
      </div>

      {/* Table */}
      <div className="card">
        <div className="card-header">
          <div>
            <div className="card-title">Alunos</div>
            <div className="card-count">{filtered.length} de {alunos.length} exibidos</div>
          </div>
          <div className="card-actions">
            <button className="btn btn-primary" onClick={openCreate}>
              <PlusIcon /> Novo Aluno
            </button>
          </div>
        </div>

        <div className="filter-bar">
          <div className="search-wrap">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input
              className="search-input"
              placeholder="Buscar por nome, CPF ou matrícula..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
          </div>
          <select className="filter-select" value={filterStatus} onChange={e => setFilterStatus(e.target.value)}>
            <option value="">Todos os status</option>
            <option value="ativa">Ativa</option>
            <option value="trancada">Trancada</option>
            <option value="cancelada">Cancelada</option>
          </select>
        </div>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>Nº Matrícula</th>
                <th>CPF</th>
                <th>Nascimento</th>
                <th>Turma</th>
                <th>Status Matríc.</th>
                <th>Situação</th>
                <th>Ações</th>
              </tr>
            </thead>
            {loading ? (
              <Loading rows={6} />
            ) : error ? (
              <tbody><tr><td colSpan={8}><ErrorBox message={error} onRetry={load} /></td></tr></tbody>
            ) : filtered.length === 0 ? (
              <tbody>
                <tr>
                  <td colSpan={8}>
                    <Empty
                      title="Nenhum aluno encontrado"
                      desc={search ? ' com esses filtros.' : ''}
                      action={<button className="btn btn-primary" onClick={openCreate}><PlusIcon /> Cadastrar Aluno</button>}
                    />
                  </td>
                </tr>
              </tbody>
            ) : (
              <tbody>
                {filtered.map(aluno => {
                  const mat = getMatricula(aluno.id)
                  return (
                    <tr key={aluno.id}>
                      <td className="td-name">{aluno.nome}</td>
                      <td className="td-mono">{aluno.matricula_numero}</td>
                      <td className="td-mono">{aluno.cpf}</td>
                      <td>{aluno.data_nascimento}</td>
                      <td>{mat ? getTurmaName(mat.turma_id) : <span style={{ color: 'var(--text-3)' }}>—</span>}</td>
                      <td>{mat ? <Badge status={mat.status} /> : <span style={{ color: 'var(--text-3)', fontSize: '12px' }}>Sem matrícula</span>}</td>
                      <td><Badge status={aluno.ativo} /></td>
                      <td>
                        <div className="td-actions">
                          <button className="btn btn-ghost btn-sm" title="Matrícula" onClick={() => openMatricula(aluno)}>
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                              <polyline points="14 2 14 8 20 8"/>
                            </svg>
                            Matrícula
                          </button>
                          <button className="btn btn-ghost btn-sm" onClick={() => openEdit(aluno)}><EditIcon /></button>
                          <button className="btn btn-ghost btn-sm" onClick={() => confirmDelete(aluno)} style={{ color: 'var(--danger)' }}><TrashIcon /></button>
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

      {/* Modal Aluno */}
      <Modal
        open={modal.open}
        title={modal.mode === 'create' ? 'Novo Aluno' : 'Editar Aluno'}
        onClose={() => setModal({ open: false })}
        footer={
          <>
            <button className="btn btn-secondary" onClick={() => setModal({ open: false })}>Cancelar</button>
            <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
              {saving ? 'Salvando...' : modal.mode === 'create' ? 'Cadastrar' : 'Salvar'}
            </button>
          </>
        }
      >
        <div className="form-grid form-grid-2">
          <div className="form-field full">
            <label>Nome completo *</label>
            <input value={form.nome} onChange={e => setForm(f => ({ ...f, nome: e.target.value }))} placeholder="Ex: João da Silva" />
          </div>
          <div className="form-field">
            <label>CPF *</label>
            <input
              value={form.cpf}
              onChange={e => setForm(f => ({ ...f, cpf: e.target.value }))}
              placeholder="Somente números"
              disabled={modal.mode === 'edit'}
            />
          </div>
          <div className="form-field">
            <label>Telefone *</label>
            <input value={form.telefone} onChange={e => setForm(f => ({ ...f, telefone: e.target.value }))} placeholder="Ex: 11999998888" />
          </div>
          <div className="form-field">
            <label>Nº Matrícula *</label>
            <input
              type="number"
              value={form.matricula_numero}
              onChange={e => setForm(f => ({ ...f, matricula_numero: e.target.value }))}
              disabled={modal.mode === 'edit'}
            />
          </div>
          <div className="form-field">
            <label>Data de Nascimento *</label>
            <input
              type="date"
              value={form.data_nascimento}
              onChange={e => setForm(f => ({ ...f, data_nascimento: e.target.value }))}
              disabled={modal.mode === 'edit'}
            />
          </div>
          <div className="form-field" style={{ justifyContent: 'flex-end', paddingBottom: '4px' }}>
            <label className="checkbox-row">
              <input type="checkbox" checked={form.ativo} onChange={e => setForm(f => ({ ...f, ativo: e.target.checked }))} />
              <span>Aluno Ativo</span>
            </label>
          </div>
        </div>
      </Modal>

      {/* Modal Matrícula */}
      <Modal
        open={matModal.open}
        title={matModal.data ? 'Editar Matrícula' : 'Nova Matrícula'}
        onClose={() => setMatModal({ open: false })}
        footer={
          <>
            <button className="btn btn-secondary" onClick={() => setMatModal({ open: false })}>Cancelar</button>
            <button className="btn btn-primary" onClick={handleSaveMatricula} disabled={savingMat}>
              {savingMat ? 'Salvando...' : 'Salvar'}
            </button>
          </>
        }
      >
        <div className="form-grid">
          <div className="form-field">
            <label>Turma *</label>
            <select value={matForm.turma_id} onChange={e => setMatForm(f => ({ ...f, turma_id: e.target.value }))}>
              <option value="">Selecione a turma</option>
              {turmas.map(t => <option key={t.id} value={t.id}>{t.nome} — {t.serie} ({t.turno})</option>)}
            </select>
          </div>
          <div className="form-field">
            <label>Data da Matrícula *</label>
            <input type="date" value={matForm.data_matricula} onChange={e => setMatForm(f => ({ ...f, data_matricula: e.target.value }))} disabled={!!matModal.data} />
          </div>
          {!matModal.data && (
            <div className="form-field">
              <label>Valor da Mensalidade (R$)</label>
              <input
                type="number" step="0.01" min="0"
                value={matForm.valor_mensalidade}
                onChange={e => setMatForm(f => ({ ...f, valor_mensalidade: e.target.value }))}
                placeholder="Ex: 950.00"
              />
              <span style={{ fontSize: '11px', color: 'var(--text-3)', marginTop: '4px', display: 'block' }}>
                12 mensalidades serão geradas automaticamente para o ano letivo da turma
              </span>
            </div>
          )}
          <div className="form-field">
            <label>Status</label>
            <select value={matForm.status} onChange={e => setMatForm(f => ({ ...f, status: e.target.value }))}>
              <option value="ativa">Ativa</option>
              <option value="trancada">Trancada</option>
              <option value="cancelada">Cancelada</option>
            </select>
          </div>
          <div className="form-field">
            <label>Observação</label>
            <textarea value={matForm.observacao || ''} onChange={e => setMatForm(f => ({ ...f, observacao: e.target.value }))} placeholder="Opcional" style={{ minHeight: '60px' }} />
          </div>
        </div>
      </Modal>

      {/* Confirm Delete */}
      <ConfirmDialog
        open={confirm.open}
        title="Excluir Aluno"
        message={`Tem certeza que deseja excluir ${confirm.nome}? Esta ação não pode ser desfeita.`}
        onConfirm={handleDelete}
        onCancel={() => setConfirm({ open: false })}
        loading={deleting}
      />
    </>
  )
}
