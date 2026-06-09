import { useState, useEffect } from 'react'
import { api } from '../api/client'
import { useToast } from '../components/Toast'
import Modal from '../components/Modal'
import { Loading, ErrorBox } from '../components/StateBox'

const EMPTY_NOTA = { aluno_id: '', disciplina_id: '', valor: '', tipo: 'prova', trimestre: '1' }
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

function InfoPill({ label, value, accent }) {
  return (
    <div style={{
      display: 'flex', flexDirection: 'column', gap: '2px',
      padding: '10px 16px',
      background: 'var(--bg-2)',
      borderRadius: '8px',
      borderLeft: accent ? `3px solid ${accent}` : '3px solid var(--border)',
      minWidth: '100px',
    }}>
      <span style={{ fontSize: '11px', color: 'var(--text-3)', fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.04em' }}>{label}</span>
      <span style={{ fontSize: '14px', fontWeight: 600, color: 'var(--text-1)' }}>{value || '—'}</span>
    </div>
  )
}

function fmt(v) {
  if (v === null || v === undefined) return <span className="nota-cell nota-dash">—</span>
  return <span className={`nota-cell ${nota_class(Number(v))}`}>{Number(v).toFixed(1)}</span>
}

function fmtVal(v) {
  if (v === null || v === undefined) return '—'
  return Number(v).toFixed(1)
}

export default function Boletim() {
  const toast = useToast()
  const [alunos, setAlunos] = useState([])
  const [disciplinas, setDisciplinas] = useState([])
  const [matriculas, setMatriculas] = useState([])
  const [turmas, setTurmas] = useState([])
  const [notas, setNotas] = useState([])
  const [frequencias, setFrequencias] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [selAluno, setSelAluno] = useState('')
  const [activeTab, setActiveTab] = useState('notas')
  const [activeBim, setActiveBim] = useState(1)

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
      const [a, d, m, t, n, f] = await Promise.all([
        api.get('/alunos'),
        api.get('/disciplinas'),
        api.get('/matriculas'),
        api.get('/turmas'),
        api.get('/notas'),
        api.get('/frequencias'),
      ])
      setAlunos(a); setDisciplinas(d); setMatriculas(m); setTurmas(t); setNotas(n); setFrequencias(f)
      if (a.length && !selAluno) setSelAluno(String(a[0].id))
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])

  const alunoId = Number(selAluno)
  const alunoObj = alunos.find(a => a.id === alunoId)
  const alunoNotas = notas.filter(n => n.aluno_id === alunoId)
  const alunoFreqs = frequencias.filter(f => f.aluno_id === alunoId)

  const alunoMatricula = matriculas.find(m => m.aluno_id === alunoId)
  const alunoTurma = turmas.find(t => t.id === alunoMatricula?.turma_id)

  const alunoDisciplinas = alunoMatricula
    ? disciplinas.filter(d => d.turma_id === alunoMatricula.turma_id)
    : disciplinas

  function getDiscipinasDoAluno(alunoIdStr) {
    const id = Number(alunoIdStr)
    const mat = matriculas.find(m => m.aluno_id === id)
    return mat ? disciplinas.filter(d => d.turma_id === mat.turma_id) : disciplinas
  }
  const nModalDiscs = getDiscipinasDoAluno(nForm.aluno_id)
  const fModalDiscs = getDiscipinasDoAluno(fForm.aluno_id)

  // Build nota grid (3 trimestres)
  function getNotaGrid() {
    const trimestres = [1, 2, 3]
    const tipos = ['prova', 'trabalho', 'recuperacao']
    return alunoDisciplinas.map(disc => {
      const row = { disc }
      trimestres.forEach(b => {
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
      const discFreqs = alunoFreqs.filter(f => f.disciplina_id === disc.id)
      row.freq_total = discFreqs.length
      row.freq_presentes = discFreqs.filter(f => f.presente).length
      row.freq_pct = discFreqs.length ? Math.round(row.freq_presentes / discFreqs.length * 100) : null
      return row
    })
  }

  const notaGrid = getNotaGrid()

  // Frequência stats
  const freqTotal = alunoFreqs.length
  const freqPresentes = alunoFreqs.filter(f => f.presente).length
  const freqFaltas = freqTotal - freqPresentes
  const freqPct = freqTotal ? Math.round(freqPresentes / freqTotal * 100) : null

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
        bimestre: Number(nForm.trimestre),
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

  const statusMatricula = alunoMatricula?.status
  const statusColor = statusMatricula === 'ativa' ? 'var(--success)' : statusMatricula === 'trancada' ? 'var(--warning)' : 'var(--danger)'

  const nascFormatted = alunoObj?.data_nascimento
    ? new Date(alunoObj.data_nascimento + 'T12:00:00').toLocaleDateString('pt-BR')
    : '—'

  return (
    <>
      {/* Selector */}
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

      {/* Student Info Panel */}
      {alunoObj && !loading && (
        <div className="card" style={{ padding: '16px 20px' }}>
          <div style={{ marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '36px', height: '36px', borderRadius: '50%',
              background: 'var(--primary)', color: '#fff',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontWeight: 700, fontSize: '15px', flexShrink: 0,
            }}>
              {alunoObj.nome.charAt(0).toUpperCase()}
            </div>
            <div>
              <div style={{ fontWeight: 700, fontSize: '15px', color: 'var(--text-1)' }}>{alunoObj.nome}</div>
              <div style={{ fontSize: '12px', color: 'var(--text-3)' }}>
                {alunoObj.ativo ? 'Aluno ativo' : 'Aluno inativo'}
              </div>
            </div>
            {statusMatricula && (
              <span style={{
                marginLeft: 'auto',
                padding: '3px 10px', borderRadius: '99px',
                fontSize: '12px', fontWeight: 600,
                background: statusColor + '22', color: statusColor,
              }}>
                Matrícula {statusMatricula}
              </span>
            )}
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            <InfoPill label="Matrícula" value={`#${alunoObj.matricula_numero}`} accent="var(--primary)" />
            <InfoPill label="Turma" value={alunoTurma?.nome} accent="var(--info, #3b82f6)" />
            <InfoPill label="Série" value={alunoTurma?.serie} />
            <InfoPill label="Turno" value={alunoTurma?.turno} />
            <InfoPill label="Ano Letivo" value={alunoTurma?.ano_letivo} />
            <InfoPill label="Nascimento" value={nascFormatted} />
            <InfoPill label="Disciplinas" value={alunoDisciplinas.length} />
          </div>
        </div>
      )}

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
            {tab === 'notas' ? 'Notas por Trimestre' : 'Frequência'}
          </button>
        ))}
      </div>

      {/* Notas */}
      {activeTab === 'notas' && (
        <>
          {/* Trimestre sub-tabs */}
          <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
            {[1,2,3].map(b => (
              <button key={b} onClick={() => setActiveBim(b)} style={{
                padding: '7px 18px', borderRadius: '8px',
                border: activeBim === b ? '2px solid var(--primary)' : '2px solid var(--border)',
                background: activeBim === b ? 'var(--primary)' : 'var(--card-bg)',
                color: activeBim === b ? '#fff' : 'var(--text-2)',
                fontWeight: 600, fontSize: '13px', cursor: 'pointer',
                fontFamily: 'Plus Jakarta Sans, sans-serif',
                transition: 'all .15s',
              }}>{b}° Trimestre</button>
            ))}
            <button onClick={() => setActiveBim(0)} style={{
              padding: '7px 18px', borderRadius: '8px',
              border: activeBim === 0 ? '2px solid var(--primary)' : '2px solid var(--border)',
              background: activeBim === 0 ? 'var(--primary)' : 'var(--card-bg)',
              color: activeBim === 0 ? '#fff' : 'var(--text-2)',
              fontWeight: 600, fontSize: '13px', cursor: 'pointer',
              fontFamily: 'Plus Jakarta Sans, sans-serif',
              transition: 'all .15s',
            }}>Resumo Geral</button>
          </div>

          {/* Bimestre detail view */}
          {activeBim > 0 && (
            <div className="card">
              <div className="card-header" style={{ marginBottom: '0' }}>
                <div>
                  <div className="card-title">{activeBim}° Trimestre</div>
                  {!loading && (
                    <div className="card-count">
                      {notaGrid.filter(r => r[`${activeBim}_prova`] !== null || r[`${activeBim}_trabalho`] !== null).length} de {notaGrid.length} disciplinas com notas
                    </div>
                  )}
                </div>
              </div>
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th style={{ textAlign: 'left' }}>Disciplina</th>
                      <th>Prova</th>
                      <th>Trabalho</th>
                      <th>Recuperação</th>
                      <th>Média do Trimestre</th>
                    </tr>
                  </thead>
                  {loading ? <Loading rows={6} /> : (
                    <tbody>
                      {notaGrid.length === 0 ? (
                        <tr><td colSpan={5} style={{ textAlign: 'center', padding: '40px', color: 'var(--text-3)' }}>
                          Selecione um aluno para ver o boletim.
                        </td></tr>
                      ) : notaGrid.map(row => (
                        <tr key={row.disc.id}>
                          <td className="td-name">{row.disc.nome}</td>
                          <td>{fmt(row[`${activeBim}_prova`])}</td>
                          <td>{fmt(row[`${activeBim}_trabalho`])}</td>
                          <td>{fmt(row[`${activeBim}_recuperacao`])}</td>
                          <td>
                            {row[`${activeBim}_media`] !== null ? (
                              <strong className={`nota-cell ${nota_class(row[`${activeBim}_media`])}`}>
                                {Number(row[`${activeBim}_media`]).toFixed(1)}
                              </strong>
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

          {/* Resumo Geral */}
          {activeBim === 0 && (
            <div className="card">
              <div className="card-header" style={{ marginBottom: '0' }}>
                <div>
                  <div className="card-title">Resumo Geral — Médias por Trimestre</div>
                  {!loading && <div className="card-count">{notaGrid.length} disciplinas</div>}
                </div>
              </div>
              <div className="table-wrap">
                <table className="boletim-table">
                  <thead>
                    <tr>
                      <th style={{ textAlign: 'left' }}>Disciplina</th>
                      <th>1° Tri</th>
                      <th>2° Tri</th>
                      <th>3° Tri</th>
                      <th>Média Final</th>
                      <th>Freq.</th>
                      <th>Situação</th>
                    </tr>
                  </thead>
                  {loading ? <Loading rows={6} /> : (
                    <tbody>
                      {notaGrid.length === 0 ? (
                        <tr><td colSpan={7} style={{ textAlign: 'center', padding: '40px', color: 'var(--text-3)' }}>
                          Selecione um aluno para ver o boletim.
                        </td></tr>
                      ) : notaGrid.map(row => {
                        const aprovado = row.media_geral !== null && row.media_geral >= 7 &&
                          (row.freq_pct === null || row.freq_pct >= 75)
                        const reprovado = row.media_geral !== null && (row.media_geral < 5 || row.freq_pct < 75)
                        const situacao = row.media_geral === null ? null : aprovado ? 'Aprovado' : reprovado ? 'Reprovado' : 'Recuperação'
                        const sitColor = situacao === 'Aprovado' ? 'nota-good' : situacao === 'Reprovado' ? 'nota-bad' : 'nota-warn'
                        return (
                          <tr key={row.disc.id}>
                            <td className="td-name">{row.disc.nome}</td>
                            <td>{fmt(row['1_media'])}</td>
                            <td>{fmt(row['2_media'])}</td>
                            <td>{fmt(row['3_media'])}</td>
                            <td>
                              {row.media_geral !== null ? (
                                <strong className={`nota-cell ${nota_class(row.media_geral)}`}>
                                  {Number(row.media_geral).toFixed(1)}
                                </strong>
                              ) : <span className="nota-cell nota-dash">—</span>}
                            </td>
                            <td>
                              {row.freq_pct !== null ? (
                                <span className={`nota-cell ${row.freq_pct >= 75 ? 'nota-good' : 'nota-bad'}`}>
                                  {row.freq_pct}%
                                </span>
                              ) : <span className="nota-cell nota-dash">—</span>}
                            </td>
                            <td>
                              {situacao ? (
                                <span className={`nota-cell ${sitColor}`} style={{ fontWeight: 600 }}>
                                  {situacao}
                                </span>
                              ) : <span className="nota-cell nota-dash">—</span>}
                            </td>
                          </tr>
                        )
                      })}
                    </tbody>
                  )}
                </table>
              </div>
            </div>
          )}
        </>
      )}

      {/* Frequência detalhada */}
      {activeTab === 'frequencia' && (
        <>
          {/* Frequência summary */}
          {!loading && freqTotal > 0 && (
            <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
              {[
                { label: 'Total de Aulas', value: freqTotal, accent: 'var(--primary)' },
                { label: 'Presenças', value: freqPresentes, accent: 'var(--success)' },
                { label: 'Faltas', value: freqFaltas, accent: freqFaltas > 0 ? 'var(--danger)' : 'var(--border)' },
                { label: '% Frequência', value: freqPct !== null ? `${freqPct}%` : '—', accent: freqPct >= 75 ? 'var(--success)' : 'var(--danger)' },
              ].map(item => (
                <div key={item.label} className="card" style={{
                  flex: '1', minWidth: '130px', padding: '14px 18px',
                  borderTop: `3px solid ${item.accent}`,
                }}>
                  <div style={{ fontSize: '11px', color: 'var(--text-3)', fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '4px' }}>{item.label}</div>
                  <div style={{ fontSize: '22px', fontWeight: 700, color: item.accent }}>{item.value}</div>
                </div>
              ))}
            </div>
          )}

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
        </>
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
            <select value={nForm.aluno_id} onChange={e => setNForm(f => ({ ...f, aluno_id: e.target.value, disciplina_id: '' }))}>
              <option value="">Selecione</option>
              {alunos.map(a => <option key={a.id} value={a.id}>{a.nome}</option>)}
            </select>
          </div>
          <div className="form-field full">
            <label>Disciplina *</label>
            <select value={nForm.disciplina_id} onChange={e => setNForm(f => ({ ...f, disciplina_id: e.target.value }))}>
              <option value="">Selecione</option>
              {nModalDiscs.map(d => <option key={d.id} value={d.id}>{d.nome}</option>)}
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
            <label>Trimestre *</label>
            <select value={nForm.trimestre} onChange={e => setNForm(f => ({ ...f, trimestre: e.target.value }))}>
              {[1,2,3].map(b => <option key={b} value={b}>{b}° Trimestre</option>)}
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
            <select value={fForm.aluno_id} onChange={e => setFForm(f => ({ ...f, aluno_id: e.target.value, disciplina_id: '' }))}>
              <option value="">Selecione</option>
              {alunos.map(a => <option key={a.id} value={a.id}>{a.nome}</option>)}
            </select>
          </div>
          <div className="form-field full">
            <label>Disciplina *</label>
            <select value={fForm.disciplina_id} onChange={e => setFForm(f => ({ ...f, disciplina_id: e.target.value }))}>
              <option value="">Selecione</option>
              {fModalDiscs.map(d => <option key={d.id} value={d.id}>{d.nome}</option>)}
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
