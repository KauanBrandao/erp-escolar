import { useState, useEffect } from 'react'
import { api } from '../api/client'
import { useToast } from '../components/Toast'
import Modal from '../components/Modal'
import { ConfirmDialog } from '../components/Modal'
import { ErrorBox, Badge } from '../components/StateBox'

const EMPTY_TURMA = { nome: '', serie: '', turno: 'Matutino', ano_letivo: new Date().getFullYear() }
const EMPTY_DISC  = { nome: '', codigo: '', carga_horaria: '', turma_id: '' }

function PlusIcon() {
  return <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
}
function EditIcon() {
  return <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
}
function TrashIcon() {
  return <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/></svg>
}

export default function Turmas() {
  const toast = useToast()
  const [turmas, setTurmas] = useState([])
  const [disciplinas, setDisciplinas] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedTurma, setSelectedTurma] = useState(null)

  // modal turma
  const [tModal, setTModal] = useState({ open: false, mode: 'create', data: null })
  const [tForm, setTForm] = useState(EMPTY_TURMA)
  const [tSaving, setTSaving] = useState(false)
  const [tConfirm, setTConfirm] = useState({ open: false, data: null })
  const [tDeleting, setTDeleting] = useState(false)

  // modal disciplina
  const [dModal, setDModal] = useState({ open: false, mode: 'create', data: null })
  const [dForm, setDForm] = useState(EMPTY_DISC)
  const [dSaving, setDSaving] = useState(false)
  const [dConfirm, setDConfirm] = useState({ open: false, data: null })
  const [dDeleting, setDDeleting] = useState(false)

  async function load() {
    try {
      setLoading(true); setError(null)
      const [t, d] = await Promise.all([api.get('/turmas'), api.get('/disciplinas')])
      setTurmas(t); setDisciplinas(d)
      if (t.length && !selectedTurma) setSelectedTurma(t[0])
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])

  const discForTurma = disciplinas.filter(d => d.turma_id === selectedTurma?.id)

  // ---- TURMA ----
  function openCreateTurma() { setTForm(EMPTY_TURMA); setTModal({ open: true, mode: 'create', data: null }) }
  function openEditTurma(t)  { setTForm({ ...t, ano_letivo: String(t.ano_letivo) }); setTModal({ open: true, mode: 'edit', data: t }) }

  async function saveTurma() {
    if (!tForm.nome || !tForm.serie || !tForm.turno || !tForm.ano_letivo) {
      toast('Preencha todos os campos obrigatórios.', 'warning'); return
    }
    try {
      setTSaving(true)
      const payload = { ...tForm, ano_letivo: Number(tForm.ano_letivo) }
      if (tModal.mode === 'create') { await api.post('/turmas', payload); toast('Turma criada!') }
      else { await api.put(`/turmas/${tModal.data.id}`, payload); toast('Turma atualizada!') }
      setTModal({ open: false }); load()
    } catch (e) { toast(e.message, 'error') }
    finally { setTSaving(false) }
  }

  async function deleteTurma() {
    try {
      setTDeleting(true)
      await api.del(`/turmas/${tConfirm.data.id}`)
      toast('Turma excluída.')
      setTConfirm({ open: false })
      if (selectedTurma?.id === tConfirm.data.id) setSelectedTurma(null)
      load()
    } catch (e) { toast(e.message, 'error') }
    finally { setTDeleting(false) }
  }

  // ---- DISCIPLINA ----
  function openCreateDisc() {
    setDForm({ ...EMPTY_DISC, turma_id: String(selectedTurma?.id || '') })
    setDModal({ open: true, mode: 'create', data: null })
  }
  function openEditDisc(d) {
    setDForm({ ...d, carga_horaria: String(d.carga_horaria), turma_id: String(d.turma_id) })
    setDModal({ open: true, mode: 'edit', data: d })
  }

  async function saveDisc() {
    if (!dForm.nome || !dForm.codigo || !dForm.carga_horaria || !dForm.turma_id) {
      toast('Preencha todos os campos obrigatórios.', 'warning'); return
    }
    try {
      setDSaving(true)
      const payload = { ...dForm, carga_horaria: Number(dForm.carga_horaria), turma_id: Number(dForm.turma_id) }
      if (dModal.mode === 'create') { await api.post('/disciplinas', payload); toast('Disciplina criada!') }
      else { await api.put(`/disciplinas/${dModal.data.id}`, payload); toast('Disciplina atualizada!') }
      setDModal({ open: false }); load()
    } catch (e) { toast(e.message, 'error') }
    finally { setDSaving(false) }
  }

  async function deleteDisc() {
    try {
      setDDeleting(true)
      await api.del(`/disciplinas/${dConfirm.data.id}`)
      toast('Disciplina excluída.')
      setDConfirm({ open: false }); load()
    } catch (e) { toast(e.message, 'error') }
    finally { setDDeleting(false) }
  }

  const TURNOS = ['Matutino', 'Vespertino', 'Noturno']

  function normalizeTurno(t) {
    const map = { 'Manhã': 'Matutino', 'Manha': 'Matutino', 'Tarde': 'Vespertino', 'Noite': 'Noturno' }
    return map[t] || t
  }

  if (error) return <ErrorBox message={error} onRetry={load} />

  return (
    <>
      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-label">Total de Turmas</div>
          <div className="stat-value">{turmas.length}</div>
          <div className="stat-sub">{[...new Set(turmas.map(t => t.ano_letivo))].sort((a,b) => b-a).join(', ')}</div>
        </div>
        {[...new Set(turmas.map(t => normalizeTurno(t.turno)))].sort().map(turno => (
          <div className="stat-card" key={turno}>
            <div className="stat-label">{turno}</div>
            <div className="stat-value">{turmas.filter(t => normalizeTurno(t.turno) === turno).length}</div>
          </div>
        ))}
        <div className="stat-card">
          <div className="stat-label">Disciplinas</div>
          <div className="stat-value" style={{ color: 'var(--primary)' }}>{disciplinas.length}</div>
          <div className="stat-sub">total no sistema</div>
        </div>
      </div>

      <div className="panel-layout">
        {/* Turmas */}
        <div className="card">
          <div className="card-header">
            <div>
              <div className="card-title">Turmas</div>
              <div className="card-count">{turmas.length} turmas cadastradas</div>
            </div>
            <div className="card-actions">
              <button className="btn btn-primary btn-sm" onClick={openCreateTurma}><PlusIcon /> Nova Turma</button>
            </div>
          </div>
          <div style={{ padding: '16px' }}>
            {loading ? (
              <div style={{ display: 'grid', gap: '10px' }}>
                {[1,2,3].map(i => <div key={i} className="skeleton" style={{ height: '80px', borderRadius: '10px' }} />)}
              </div>
            ) : turmas.length === 0 ? (
              <div className="state-box">
                <p>Nenhuma turma cadastrada.</p>
                <button className="btn btn-primary btn-sm" onClick={openCreateTurma}><PlusIcon /> Criar Turma</button>
              </div>
            ) : (
              <div className="turmas-grid">
                {turmas.map(t => (
                  <div
                    key={t.id}
                    className={`turma-card${selectedTurma?.id === t.id ? ' selected' : ''}`}
                    onClick={() => setSelectedTurma(t)}
                  >
                    <div className="turma-card-name">{t.nome}</div>
                    <div className="turma-card-meta">{t.serie} · {t.turno}</div>
                    <div className="turma-card-bottom">
                      <span style={{ fontSize: '11px', color: 'var(--text-3)' }}>{t.ano_letivo}</span>
                      <div className="turma-card-actions" onClick={e => e.stopPropagation()}>
                        <button className="btn btn-ghost btn-sm" onClick={() => openEditTurma(t)}><EditIcon /></button>
                        <button className="btn btn-ghost btn-sm" style={{ color: 'var(--danger)' }} onClick={() => setTConfirm({ open: true, data: t })}><TrashIcon /></button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Disciplinas */}
        <div className="card">
          <div className="card-header">
            <div>
              <div className="card-title">Disciplinas</div>
              <div className="card-count">
                {selectedTurma ? `${selectedTurma.nome} — ${discForTurma.length} disciplinas` : 'Selecione uma turma'}
              </div>
            </div>
            {selectedTurma && (
              <div className="card-actions">
                <button className="btn btn-primary btn-sm" onClick={openCreateDisc}><PlusIcon /> Nova Disciplina</button>
              </div>
            )}
          </div>
          <div className="table-wrap">
            {!selectedTurma ? (
              <div className="state-box">
                <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" style={{ opacity: .35 }}>
                  <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
                </svg>
                <p>Selecione uma turma ao lado para ver as disciplinas</p>
              </div>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Disciplina</th>
                    <th>Código</th>
                    <th>Carga Horária</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {discForTurma.length === 0 ? (
                    <tr>
                      <td colSpan={4}>
                        <div className="state-box" style={{ padding: '32px' }}>
                          <p>Nenhuma disciplina nesta turma.</p>
                          <button className="btn btn-primary btn-sm" onClick={openCreateDisc}><PlusIcon /> Adicionar</button>
                        </div>
                      </td>
                    </tr>
                  ) : discForTurma.map(d => (
                    <tr key={d.id}>
                      <td className="td-name">{d.nome}</td>
                      <td className="td-mono">{d.codigo}</td>
                      <td>{d.carga_horaria}h</td>
                      <td>
                        <div className="td-actions">
                          <button className="btn btn-ghost btn-sm" onClick={() => openEditDisc(d)}><EditIcon /></button>
                          <button className="btn btn-ghost btn-sm" style={{ color: 'var(--danger)' }} onClick={() => setDConfirm({ open: true, data: d })}><TrashIcon /></button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>

      {/* Modal Turma */}
      <Modal
        open={tModal.open}
        title={tModal.mode === 'create' ? 'Nova Turma' : 'Editar Turma'}
        onClose={() => setTModal({ open: false })}
        footer={<>
          <button className="btn btn-secondary" onClick={() => setTModal({ open: false })}>Cancelar</button>
          <button className="btn btn-primary" onClick={saveTurma} disabled={tSaving}>{tSaving ? 'Salvando...' : 'Salvar'}</button>
        </>}
      >
        <div className="form-grid form-grid-2">
          <div className="form-field">
            <label>Nome da Turma *</label>
            <input value={tForm.nome} onChange={e => setTForm(f => ({ ...f, nome: e.target.value }))} placeholder="Ex: 9° Ano A" />
          </div>
          <div className="form-field">
            <label>Série *</label>
            <input value={tForm.serie} onChange={e => setTForm(f => ({ ...f, serie: e.target.value }))} placeholder="Ex: 9° Ano" />
          </div>
          <div className="form-field">
            <label>Turno *</label>
            <select value={tForm.turno} onChange={e => setTForm(f => ({ ...f, turno: e.target.value }))}>
              {TURNOS.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <div className="form-field">
            <label>Ano Letivo *</label>
            <input type="number" value={tForm.ano_letivo} onChange={e => setTForm(f => ({ ...f, ano_letivo: e.target.value }))} min="2000" max="2100" />
          </div>
        </div>
      </Modal>

      {/* Modal Disciplina */}
      <Modal
        open={dModal.open}
        title={dModal.mode === 'create' ? 'Nova Disciplina' : 'Editar Disciplina'}
        onClose={() => setDModal({ open: false })}
        footer={<>
          <button className="btn btn-secondary" onClick={() => setDModal({ open: false })}>Cancelar</button>
          <button className="btn btn-primary" onClick={saveDisc} disabled={dSaving}>{dSaving ? 'Salvando...' : 'Salvar'}</button>
        </>}
      >
        <div className="form-grid form-grid-2">
          <div className="form-field full">
            <label>Nome da Disciplina *</label>
            <input value={dForm.nome} onChange={e => setDForm(f => ({ ...f, nome: e.target.value }))} placeholder="Ex: Matemática" />
          </div>
          <div className="form-field">
            <label>Código *</label>
            <input value={dForm.codigo} onChange={e => setDForm(f => ({ ...f, codigo: e.target.value }))} placeholder="Ex: MAT001" />
          </div>
          <div className="form-field">
            <label>Carga Horária (h) *</label>
            <input type="number" value={dForm.carga_horaria} onChange={e => setDForm(f => ({ ...f, carga_horaria: e.target.value }))} min="1" placeholder="Ex: 120" />
          </div>
          <div className="form-field full">
            <label>Turma *</label>
            <select value={dForm.turma_id} onChange={e => setDForm(f => ({ ...f, turma_id: e.target.value }))}>
              <option value="">Selecione a turma</option>
              {turmas.map(t => <option key={t.id} value={t.id}>{t.nome}</option>)}
            </select>
          </div>
        </div>
      </Modal>

      <ConfirmDialog open={tConfirm.open} title="Excluir Turma"
        message={`Excluir "${tConfirm.data?.nome}"? As disciplinas vinculadas também serão afetadas.`}
        onConfirm={deleteTurma} onCancel={() => setTConfirm({ open: false })} loading={tDeleting} />

      <ConfirmDialog open={dConfirm.open} title="Excluir Disciplina"
        message={`Excluir "${dConfirm.data?.nome}"?`}
        onConfirm={deleteDisc} onCancel={() => setDConfirm({ open: false })} loading={dDeleting} />
    </>
  )
}
