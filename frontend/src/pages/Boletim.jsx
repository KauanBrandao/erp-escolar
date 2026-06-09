import { useState, useEffect } from 'react'
import { api } from '../api/client'
import { useToast } from '../components/Toast'
import Modal from '../components/Modal'
import { Loading, ErrorBox } from '../components/StateBox'

const EMPTY_NOTA = { aluno_id: '', disciplina_id: '', valor: '', tipo: 'prova', bimestre: '1' }
const EMPTY_FREQ = { aluno_id: '', disciplina_id: '', data_aula: '', presente: true, justificativa: '' }

function nota_class(v) {
  if (v === null || v === undefined) return 'nota-dash'
  if (v >= 7) return 'nota-good'
  if (v >= 5) return 'nota-warn'
  return 'nota-bad'
}

function PlusIcon() {
  return <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
}

export default function Boletim() {
  const toast = useToast()
  const [alunos, setAlunos] = useState([])
  const [disciplinas, setDisciplinas] = useState([])
  const [matriculas, setMatriculas] = useState([])
  const [notas, setNotas] = useState([])
  const [frequencias, setFrequencias] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [selAluno, setSelAluno] = useState('')
  const [activeTab, setActiveTab] = useState('notas')

  // modal nota
  const [nModal, setNModal] = useState({ open: false })
  const [nForm, setNForm] = useState(EMPTY_NOTA)
  const [nSaving, setNSaving] = useState(false)

  // modal frequência
  const [fModal, setFModal] = useState({ open: false })
  const [fForm, setFForm] = useState(EMPTY_FREQ)
  const [fSaving, setFSaving] = useState(false)

  async function load() {
    try {
      setLoading(true); setError(null)
      const [a, d, m, n, f] = await Promise.all([
        api.get('/alunos'),
        api.get('/disciplinas'),
        api.get('/matriculas'),
        api.get('/notas'),
        api.get('/frequencias'),
      ])
      setAlunos(a); setDisciplinas(d); setMatriculas(m); setNotas(n); setFrequencias(f)
      if (a.length && !selAluno) setSelAluno(String(a[0].id))
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])

  const alunoId = Number(selAluno)
  const alunoNotas = notas.filter(n => n.aluno_id === alunoId)
  const alunoFreqs = frequencias.filter(f => f.aluno_id === alunoId)

  // Disciplinas apenas da turma do aluno selecionado
  const alunoMatricula = matriculas.find(m => m.aluno_id === alunoId)
  const alunoDisciplinas = alunoMatricula
    ? disciplinas.filter(d => d.turma_id === alunoMatricula.turma_id)
    : disciplinas

  // Agrupar notas por disciplina + bimestre
  function getNotaGrid() {
    const bimestres = [1, 2, 3, 4]
    const tipos = ['prova', 'trabalho', 'recuperacao']

    return alunoDisciplinas.map(disc => {
      const row = { disc }
      bimestres.forEach(b => {
        tipos.forEach(tipo => {
          const n = alunoNotas.find(n => n.disciplina_id === disc.id && n.bimestre === b && n.tipo === tipo)
          row[`${b}_${tipo}`] = n?.valor ?? null
        })
        const bNotas = alunoNotas.filter(n => n.disciplina_id === disc.id && n.bimestre === b)
        row[`${b}_media`] = bNotas.length
          ? bNotas.reduce((s, n) => s + Number(n.valor), 0) / bNotas.length
          : null
      })
      const allNotas = alunoNotas.filter(n => n.disciplina_id === disc.id)
      row.media_geral = allNotas.length
        ? allNotas.reduce((s, n) => s + Number(n.valor), 0) / allNotas.length
        : null

      // Frequência
      const discFreqs = alunoFreqs.filter(f => f.disciplina_id === disc.id)
      row.freq_total = discFreqs.length
      row.freq_presentes = discFreqs.filter(f => f.presente).length
      row.freq_pct = discFreqs.length ? Math.round(row.freq_presentes / discFreqs.length * 100) : null

      return row
    })
  }

  const notaGrid = getNotaGrid()

  function fmt(v) {
    if (v === null || v === undefined) return <span className="nota-cell nota-dash">—</span>
    return <span className={`nota-cell ${nota_class(Number(v))}`}>{Number(v).toFixed(1)}</span>
  }

  // ---- SALVAR NOTA ----
  async function saveNota() {
    if (!nForm.aluno_id || !nForm.disciplina_id || !nForm.valor) {
      toast('Preencha todos os campos obrigatórios.', 'warning'); return
    }
    try {
      setNSaving(true)
      await api.post('/notas', {
        aluno_id: Number(nForm.aluno_id),
        disciplina_id: Number(nForm.disciplina_id),
        valor: Number(nForm.valor),
        tipo: nForm.tipo,
        bimestre: Number(nForm.bimestre),
      })
      toast('Nota lançada!'); setNModal({ open: false }); load()
    } catch (e) { toast(e.message, 'error') }
    finally { setNSaving(false) }
  }

  // ---- SALVAR FREQUÊNCIA ----
  async function saveFreq() {
    if (!fForm.aluno_id || !fForm.disciplina_id || !fForm.data_aula) {
      toast('Preencha todos os campos obrigatórios.', 'warning'); return
    }
    try {
      setFSaving(true)
      await api.post('/frequencias', {
        aluno_id: Number(fForm.aluno_id),
        disciplina_id: Number(fForm.disciplina_id),
        data_aula: fForm.data_aula,
        presente: fForm.presente,
        justificativa: fForm.justificativa || null,
      })
      toast('Frequência registrada!'); setFModal({ open: false }); load()
    } catch (e) { toast(e.message, 'error') }
    finally { setFSaving(false) }
  }

  if (error) return <ErrorBox message={error} onRetry={load} />

  return (
    <>
      {/* Controls */}
      <div className="card" style={{ padding: '16px 20px' }}>
        <div className="boletim-controls">
          <div style={{ flex: 1, minWidth: '200px', maxWidth: '340px' }}>
            <label style={{ display: 'block', marginBottom: '6px' }}>Aluno</label>
            <select className="boletim-select" value={selAluno} onChange={e => setSelAluno(e.target.value)}>
              {alunos.map(a => <option key={a.id} value={a.id}>{a.nome}</option>)}
            </select>
          </div>
          <div style={{ marginLeft: 'auto', display: 'flex', gap: '8px' }}>
            <button className="btn btn-secondary" onClick={() => {
              setNForm({ ...EMPTY_NOTA, aluno_id: String(selAluno) })
              setNModal({ open: true })
            }}><PlusIcon /> Lançar Nota</button>
            <button className="btn btn-secondary" onClick={() => {
              setFForm({ ...EMPTY_FREQ, aluno_id: String(selAluno), data_aula: new Date().toISOString().slice(0,10) })
              setFModal({ open: true })
            }}><PlusIcon /> Registrar Frequência</button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '4px', borderBottom: '2px solid var(--border)', paddingBottom: '0' }}>
        {['notas', 'frequencia'].map(tab => (
          <button key={tab} onClick={() => setActiveTab(tab)} style={{
            background: 'none', border: 'none', cursor: 'pointer',
            padding: '8px 18px',
            fontSize: '13.5px', fontWeight: activeTab === tab ? 600 : 400,
            color: activeTab === tab ? 'var(--primary)' : 'var(--text-2)',
            borderBottom: activeTab === tab ? '2px solid var(--primary)' : '2px solid transparent',
            marginBottom: '-2px',
            fontFamily: 'Plus Jakarta Sans, sans-serif',
            transition: 'color .15s',
          }}>
            {tab === 'notas' ? 'Notas por Bimestre' : 'Frequência'}
          </button>
        ))}
      </div>

      {/* Notas */}
      {activeTab === 'notas' && (
        <div className="card">
          <div className="table-wrap">
            <table className="boletim-table">
              <thead>
                <tr>
                  <th style={{ textAlign: 'left' }}>Disciplina</th>
                  {[1,2,3,4].map(b => (
                    <th key={b} colSpan={3}>{b}° Bim</th>
                  ))}
                  <th>Média Final</th>
                  <th>Freq.</th>
                </tr>
                <tr>
                  <th></th>
                  {[1,2,3,4].map(b => (
                    <>
                      <th key={`${b}_p`} style={{ fontSize: '10px', color: 'var(--text-3)' }}>Prova</th>
                      <th key={`${b}_t`} style={{ fontSize: '10px', color: 'var(--text-3)' }}>Trab.</th>
                      <th key={`${b}_r`} style={{ fontSize: '10px', color: 'var(--text-3)' }}>Recup.</th>
                    </>
                  ))}
                  <th></th>
                  <th></th>
                </tr>
              </thead>
              {loading ? <Loading rows={6} /> : (
                <tbody>
                  {notaGrid.length === 0 ? (
                    <tr><td colSpan={12} style={{ textAlign: 'center', padding: '40px', color: 'var(--text-3)' }}>
                      Selecione um aluno para ver o boletim.
                    </td></tr>
                  ) : notaGrid.map(row => (
                    <tr key={row.disc.id}>
                      <td className="td-name">{row.disc.nome}</td>
                      {[1,2,3,4].map(b => (
                        <>
                          <td key={`${b}_p`}>{fmt(row[`${b}_prova`])}</td>
                          <td key={`${b}_t`}>{fmt(row[`${b}_trabalho`])}</td>
                          <td key={`${b}_r`}>{fmt(row[`${b}_recuperacao`])}</td>
                        </>
                      ))}
                      <td>
                        <strong className={`nota-cell ${nota_class(row.media_geral)}`}>
                          {row.media_geral !== null ? Number(row.media_geral).toFixed(1) : '—'}
                        </strong>
                      </td>
                      <td>
                        {row.freq_pct !== null ? (
                          <span className={`nota-cell ${row.freq_pct >= 75 ? 'nota-good' : 'nota-bad'}`}>
                            {row.freq_pct}%
                          </span>
                        ) : <span className="nota-cell nota-dash">—</span>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              )}
            </table>
          </div>
        </div>
      )}

      {/* Frequência detalhada */}
      {activeTab === 'frequencia' && (
        <div className="card">
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Data</th>
                  <th>Disciplina</th>
                  <th>Situação</th>
                  <th>Justificativa</th>
                </tr>
              </thead>
              {loading ? <Loading rows={6} /> : (
                <tbody>
                  {alunoFreqs.length === 0 ? (
                    <tr><td colSpan={4} style={{ textAlign: 'center', padding: '40px', color: 'var(--text-3)' }}>
                      Nenhuma frequência registrada para este aluno.
                    </td></tr>
                  ) : alunoFreqs.sort((a, b) => b.data_aula?.localeCompare(a.data_aula)).map(f => {
                    const disc = disciplinas.find(d => d.id === f.disciplina_id)
                    return (
                      <tr key={f.id}>
                        <td className="td-mono">{f.data_aula}</td>
                        <td>{disc?.nome || '—'}</td>
                        <td>
                          <span className={`badge ${f.presente ? 'badge-success' : 'badge-danger'}`}>
                            {f.presente ? 'Presente' : 'Ausente'}
                          </span>
                        </td>
                        <td style={{ color: 'var(--text-2)', fontSize: '13px' }}>{f.justificativa || '—'}</td>
                      </tr>
                    )
                  })}
                </tbody>
              )}
            </table>
          </div>
        </div>
      )}

      {/* Modal Nota */}
      <Modal open={nModal.open} title="Lançar Nota" onClose={() => setNModal({ open: false })}
        footer={<>
          <button className="btn btn-secondary" onClick={() => setNModal({ open: false })}>Cancelar</button>
          <button className="btn btn-primary" onClick={saveNota} disabled={nSaving}>{nSaving ? 'Salvando...' : 'Lançar'}</button>
        </>}
      >
        <div className="form-grid form-grid-2">
          <div className="form-field full">
            <label>Aluno *</label>
            <select value={nForm.aluno_id} onChange={e => setNForm(f => ({ ...f, aluno_id: e.target.value }))}>
              <option value="">Selecione</option>
              {alunos.map(a => <option key={a.id} value={a.id}>{a.nome}</option>)}
            </select>
          </div>
          <div className="form-field full">
            <label>Disciplina *</label>
            <select value={nForm.disciplina_id} onChange={e => setNForm(f => ({ ...f, disciplina_id: e.target.value }))}>
              <option value="">Selecione</option>
              {disciplinas.map(d => <option key={d.id} value={d.id}>{d.nome}</option>)}
            </select>
          </div>
          <div className="form-field">
            <label>Tipo *</label>
            <select value={nForm.tipo} onChange={e => setNForm(f => ({ ...f, tipo: e.target.value }))}>
              <option value="prova">Prova</option>
              <option value="trabalho">Trabalho</option>
              <option value="recuperacao">Recuperação</option>
            </select>
          </div>
          <div className="form-field">
            <label>Bimestre *</label>
            <select value={nForm.bimestre} onChange={e => setNForm(f => ({ ...f, bimestre: e.target.value }))}>
              {[1,2,3,4].map(b => <option key={b} value={b}>{b}° Bimestre</option>)}
            </select>
          </div>
          <div className="form-field full">
            <label>Valor (0 a 10) *</label>
            <input type="number" step="0.1" min="0" max="10" value={nForm.valor}
              onChange={e => setNForm(f => ({ ...f, valor: e.target.value }))} placeholder="Ex: 8.5" />
          </div>
        </div>
      </Modal>

      {/* Modal Frequência */}
      <Modal open={fModal.open} title="Registrar Frequência" onClose={() => setFModal({ open: false })}
        footer={<>
          <button className="btn btn-secondary" onClick={() => setFModal({ open: false })}>Cancelar</button>
          <button className="btn btn-primary" onClick={saveFreq} disabled={fSaving}>{fSaving ? 'Salvando...' : 'Registrar'}</button>
        </>}
      >
        <div className="form-grid form-grid-2">
          <div className="form-field full">
            <label>Aluno *</label>
            <select value={fForm.aluno_id} onChange={e => setFForm(f => ({ ...f, aluno_id: e.target.value }))}>
              <option value="">Selecione</option>
              {alunos.map(a => <option key={a.id} value={a.id}>{a.nome}</option>)}
            </select>
          </div>
          <div className="form-field full">
            <label>Disciplina *</label>
            <select value={fForm.disciplina_id} onChange={e => setFForm(f => ({ ...f, disciplina_id: e.target.value }))}>
              <option value="">Selecione</option>
              {disciplinas.map(d => <option key={d.id} value={d.id}>{d.nome}</option>)}
            </select>
          </div>
          <div className="form-field">
            <label>Data da Aula *</label>
            <input type="date" value={fForm.data_aula} onChange={e => setFForm(f => ({ ...f, data_aula: e.target.value }))} />
          </div>
          <div className="form-field" style={{ justifyContent: 'flex-end' }}>
            <label className="checkbox-row">
              <input type="checkbox" checked={fForm.presente} onChange={e => setFForm(f => ({ ...f, presente: e.target.checked }))} />
              <span>Presente</span>
            </label>
          </div>
          <div className="form-field full">
            <label>Justificativa</label>
            <textarea value={fForm.justificativa} onChange={e => setFForm(f => ({ ...f, justificativa: e.target.value }))} placeholder="Opcional — preencha em caso de ausência justificada" />
          </div>
        </div>
      </Modal>
    </>
  )
}
