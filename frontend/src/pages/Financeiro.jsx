import { useState, useEffect } from 'react'
import { api } from '../api/client'
import { useToast } from '../components/Toast'
import Modal from '../components/Modal'
import { ConfirmDialog } from '../components/Modal'
import { Loading, ErrorBox, Badge } from '../components/StateBox'

const MESES = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
const FORMAS = ['PIX', 'Boleto', 'Cartão de Crédito', 'Cartão de Débito', 'Transferência', 'Dinheiro']

function PlusIcon() {
  return <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
}

const EMPTY_MENS = { aluno_id: '', mes: new Date().getMonth() + 1, ano: new Date().getFullYear(), valor: '' }
const EMPTY_PAG  = { mensalidade_id: '', data_pagamento: new Date().toISOString().slice(0,10), valor_pago: '', forma_pagamento: 'PIX', comprovante: '' }

export default function Financeiro() {
  const toast = useToast()
  const [mensalidades, setMensalidades] = useState([])
  const [pagamentos, setPagamentos] = useState([])
  const [alunos, setAlunos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [search, setSearch] = useState('')
  const [filterStatus, setFilterStatus] = useState('')
  const [filterMes, setFilterMes] = useState('')

  const [mModal, setMModal] = useState({ open: false })
  const [mForm, setMForm] = useState(EMPTY_MENS)
  const [mSaving, setMSaving] = useState(false)

  const [pModal, setPModal] = useState({ open: false, mens: null })
  const [pForm, setPForm] = useState(EMPTY_PAG)
  const [pSaving, setPSaving] = useState(false)

  const [mConfirm, setMConfirm] = useState({ open: false, id: null })
  const [mDeleting, setMDeleting] = useState(false)

  async function load() {
    try {
      setLoading(true); setError(null)
      const [m, p, a] = await Promise.all([
        api.get('/mensalidades'),
        api.get('/pagamentos'),
        api.get('/alunos'),
      ])
      setMensalidades(m); setPagamentos(p); setAlunos(a)
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])

  function getAluno(id) { return alunos.find(a => a.id === id) }
  function getPagamento(mensId) { return pagamentos.find(p => p.mensalidade_id === mensId) }

  function getMensStatus(mens) {
    const pag = getPagamento(mens.id)
    if (pag) return 'pago'
    const venc = new Date(mens.vencimento)
    if (venc < new Date()) return 'atrasado'
    return 'pendente'
  }

  const filtered = mensalidades.filter(m => {
    const aluno = getAluno(m.aluno_id)
    const q = search.toLowerCase()
    const matchSearch = !q || aluno?.nome.toLowerCase().includes(q)
    const status = getMensStatus(m)
    const matchStatus = !filterStatus || status === filterStatus
    const matchMes = !filterMes || m.mes === Number(filterMes)
    return matchSearch && matchStatus && matchMes
  })

  // Resumo financeiro — baseado nos registros filtrados
  const totalValor = filtered.reduce((s, m) => s + m.valor, 0)
  const totalRecebido = filtered.reduce((s, m) => {
    const p = getPagamento(m.id)
    return s + (p ? Number(p.valor_pago) : 0)
  }, 0)
  const totalPendente = totalValor - totalRecebido

  // ---- MENSALIDADE ----
  async function saveMens() {
    if (!mForm.aluno_id || !mForm.valor) { toast('Preencha os campos obrigatórios.', 'warning'); return }
    try {
      setMSaving(true)
      await api.post('/mensalidades', {
        aluno_id: Number(mForm.aluno_id),
        mes: Number(mForm.mes),
        ano: Number(mForm.ano),
        valor: Number(mForm.valor),
      })
      toast('Mensalidade criada!'); setMModal({ open: false }); load()
    } catch (e) { toast(e.message, 'error') }
    finally { setMSaving(false) }
  }

  async function deleteMens() {
    try {
      setMDeleting(true)
      await api.del(`/mensalidades/${mConfirm.id}`)
      toast('Mensalidade excluída.'); setMConfirm({ open: false }); load()
    } catch (e) { toast(e.message, 'error') }
    finally { setMDeleting(false) }
  }

  // ---- PAGAMENTO ----
  function openPagamento(mens) {
    setPForm({ ...EMPTY_PAG, mensalidade_id: String(mens.id), valor_pago: String(mens.valor) })
    setPModal({ open: true, mens })
  }

  async function savePag() {
    if (!pForm.valor_pago || !pForm.forma_pagamento) { toast('Preencha os campos obrigatórios.', 'warning'); return }
    try {
      setPSaving(true)
      await api.post('/pagamentos', {
        mensalidade_id: Number(pForm.mensalidade_id),
        data_pagamento: pForm.data_pagamento,
        valor_pago: Number(pForm.valor_pago),
        forma_pagamento: pForm.forma_pagamento,
        comprovante: pForm.comprovante || null,
      })
      toast('Pagamento registrado!'); setPModal({ open: false }); load()
    } catch (e) { toast(e.message, 'error') }
    finally { setPSaving(false) }
  }

  function fmt(v) { return `R$ ${Number(v).toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.')}` }

  if (error) return <ErrorBox message={error} onRetry={load} />

  return (
    <>
      {/* Resumo */}
      <div className="fin-summary">
        <div className="fin-card">
          <div className="fin-label">Total a Receber</div>
          <div className="fin-value">{fmt(totalValor)}</div>
          <div className="fin-sub">{mensalidades.length} mensalidades</div>
        </div>
        <div className="fin-card">
          <div className="fin-label">Total Recebido</div>
          <div className="fin-value green">{fmt(totalRecebido)}</div>
          <div className="fin-sub">{totalValor > 0 ? Math.round(totalRecebido / totalValor * 100) : 0}% arrecadado</div>
        </div>
        <div className="fin-card">
          <div className="fin-label">Pendente / Em Atraso</div>
          <div className="fin-value red">{fmt(totalPendente)}</div>
          <div className="fin-sub">
            {filtered.filter(m => getMensStatus(m) === 'atrasado').length} em atraso
          </div>
        </div>
      </div>

      {/* Tabela */}
      <div className="card">
        <div className="card-header">
          <div>
            <div className="card-title">Mensalidades</div>
            <div className="card-count">{filtered.length} de {mensalidades.length} registros</div>
          </div>
          <div className="card-actions">
            <button className="btn btn-primary" onClick={() => { setMForm(EMPTY_MENS); setMModal({ open: true }) }}>
              <PlusIcon /> Nova Mensalidade
            </button>
          </div>
        </div>

        <div className="filter-bar">
          <div className="search-wrap">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input className="search-input" placeholder="Buscar aluno..." value={search} onChange={e => setSearch(e.target.value)} />
          </div>
          <select className="filter-select" value={filterMes} onChange={e => setFilterMes(e.target.value)}>
            <option value="">Todos os meses</option>
            {MESES.map((m, i) => <option key={i+1} value={i+1}>{m}</option>)}
          </select>
          <select className="filter-select" value={filterStatus} onChange={e => setFilterStatus(e.target.value)}>
            <option value="">Todos os status</option>
            <option value="pago">Pago</option>
            <option value="pendente">Pendente</option>
            <option value="atrasado">Atrasado</option>
          </select>
        </div>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Aluno</th>
                <th>Competência</th>
                <th>Vencimento</th>
                <th>Valor</th>
                <th>Forma Pag.</th>
                <th>Data Pag.</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            {loading ? <Loading rows={6} /> : (
              <tbody>
                {filtered.length === 0 ? (
                  <tr><td colSpan={8}>
                    <div className="state-box">
                      <p>Nenhuma mensalidade encontrada.</p>
                      <button className="btn btn-primary" onClick={() => setMModal({ open: true })}><PlusIcon /> Nova Mensalidade</button>
                    </div>
                  </td></tr>
                ) : filtered.map(m => {
                  const aluno = getAluno(m.aluno_id)
                  const pag = getPagamento(m.id)
                  const status = getMensStatus(m)
                  return (
                    <tr key={m.id}>
                      <td className="td-name">{aluno?.nome || '—'}</td>
                      <td>{MESES[m.mes - 1]}/{m.ano}</td>
                      <td className="td-mono">{m.vencimento}</td>
                      <td className="td-mono">{fmt(m.valor)}</td>
                      <td>{pag?.forma_pagamento || <span style={{ color: 'var(--text-3)' }}>—</span>}</td>
                      <td className="td-mono">{pag?.data_pagamento || <span style={{ color: 'var(--text-3)' }}>—</span>}</td>
                      <td><Badge status={status} /></td>
                      <td>
                        <div className="td-actions">
                          {!pag && (
                            <button className="btn btn-primary btn-sm" onClick={() => openPagamento(m)}>
                              Registrar Pag.
                            </button>
                          )}
                          <button className="btn btn-ghost btn-sm" style={{ color: 'var(--danger)' }}
                            onClick={() => setMConfirm({ open: true, id: m.id })}>
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                              <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>
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

      {/* Modal Nova Mensalidade */}
      <Modal open={mModal.open} title="Nova Mensalidade" onClose={() => setMModal({ open: false })}
        footer={<>
          <button className="btn btn-secondary" onClick={() => setMModal({ open: false })}>Cancelar</button>
          <button className="btn btn-primary" onClick={saveMens} disabled={mSaving}>{mSaving ? 'Salvando...' : 'Criar'}</button>
        </>}
      >
        <div className="form-grid form-grid-2">
          <div className="form-field full">
            <label>Aluno *</label>
            <select value={mForm.aluno_id} onChange={e => setMForm(f => ({ ...f, aluno_id: e.target.value }))}>
              <option value="">Selecione o aluno</option>
              {alunos.map(a => <option key={a.id} value={a.id}>{a.nome}</option>)}
            </select>
          </div>
          <div className="form-field">
            <label>Mês *</label>
            <select value={mForm.mes} onChange={e => setMForm(f => ({ ...f, mes: Number(e.target.value) }))}>
              {MESES.map((m, i) => <option key={i+1} value={i+1}>{m}</option>)}
            </select>
          </div>
          <div className="form-field">
            <label>Ano *</label>
            <input type="number" value={mForm.ano} onChange={e => setMForm(f => ({ ...f, ano: e.target.value }))} min="2000" max="2100" />
          </div>
          <div className="form-field full">
            <label>Valor (R$) *</label>
            <input type="number" step="0.01" min="0" value={mForm.valor} onChange={e => setMForm(f => ({ ...f, valor: e.target.value }))} placeholder="Ex: 950.00" />
          </div>
        </div>
      </Modal>

      {/* Modal Registrar Pagamento */}
      <Modal open={pModal.open} title={`Registrar Pagamento — ${getAluno(pModal.mens?.aluno_id)?.nome || ''}`}
        onClose={() => setPModal({ open: false })}
        footer={<>
          <button className="btn btn-secondary" onClick={() => setPModal({ open: false })}>Cancelar</button>
          <button className="btn btn-primary" onClick={savePag} disabled={pSaving}>{pSaving ? 'Salvando...' : 'Confirmar Pagamento'}</button>
        </>}
      >
        <div className="form-grid form-grid-2">
          <div className="form-field">
            <label>Data do Pagamento *</label>
            <input type="date" value={pForm.data_pagamento} onChange={e => setPForm(f => ({ ...f, data_pagamento: e.target.value }))} />
          </div>
          <div className="form-field">
            <label>Valor Pago (R$) *</label>
            <input type="number" step="0.01" min="0" value={pForm.valor_pago} onChange={e => setPForm(f => ({ ...f, valor_pago: e.target.value }))} />
          </div>
          <div className="form-field full">
            <label>Forma de Pagamento *</label>
            <select value={pForm.forma_pagamento} onChange={e => setPForm(f => ({ ...f, forma_pagamento: e.target.value }))}>
              {FORMAS.map(f => <option key={f} value={f}>{f}</option>)}
            </select>
          </div>
          <div className="form-field full">
            <label>Comprovante / Observação</label>
            <input value={pForm.comprovante} onChange={e => setPForm(f => ({ ...f, comprovante: e.target.value }))} placeholder="Nº do comprovante ou observação (opcional)" />
          </div>
        </div>
      </Modal>

      <ConfirmDialog open={mConfirm.open} title="Excluir Mensalidade"
        message="Excluir esta mensalidade? Os pagamentos vinculados também podem ser afetados."
        onConfirm={deleteMens} onCancel={() => setMConfirm({ open: false })} loading={mDeleting} />
    </>
  )
}
