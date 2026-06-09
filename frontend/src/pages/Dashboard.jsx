import { useState, useEffect } from 'react'
import { api } from '../api/client'

/* ── helpers ── */
function avg(arr) {
  if (!arr.length) return null
  return arr.reduce((s, n) => s + Number(n), 0) / arr.length
}

function fmt(v, decimals = 1) {
  if (v === null || v === undefined) return '—'
  return Number(v).toFixed(decimals)
}

function fmtBRL(v) {
  return v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function notaClass(v) {
  if (v === null) return '#94a3b8'
  if (v >= 7) return 'var(--success)'
  if (v >= 5) return 'var(--warning)'
  return 'var(--danger)'
}

/* ── sub-components ── */
function StatCard({ label, value, sub, color, icon }) {
  return (
    <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '16px', padding: '20px 24px' }}>
      <div style={{
        width: 52, height: 52, borderRadius: 14,
        background: color + '18', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
      }}>
        <span style={{ fontSize: 24 }}>{icon}</span>
      </div>
      <div style={{ minWidth: 0 }}>
        <div style={{ fontSize: 26, fontWeight: 700, color: 'var(--text)', lineHeight: 1.1 }}>{value}</div>
        <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text)', marginTop: 2 }}>{label}</div>
        <div style={{ fontSize: 11, color: 'var(--text-3)', marginTop: 1 }}>{sub}</div>
      </div>
    </div>
  )
}

function Bar({ value, max, color }) {
  const pct = max > 0 ? Math.min((value / max) * 100, 100) : 0
  return (
    <div style={{ background: 'var(--border)', borderRadius: 6, height: 10, overflow: 'hidden' }}>
      <div style={{ width: `${pct}%`, height: '100%', background: color, borderRadius: 6, transition: 'width .5s ease' }} />
    </div>
  )
}

function SectionTitle({ children }) {
  return (
    <div style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-2)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 16 }}>
      {children}
    </div>
  )
}

function Skeleton() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
        {[0,1,2,3].map(i => (
          <div key={i} className="card" style={{ height: 92, background: 'var(--surface-2)' }} />
        ))}
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div className="card" style={{ height: 280 }} />
        <div className="card" style={{ height: 280 }} />
      </div>
      <div className="card" style={{ height: 200 }} />
    </div>
  )
}

/* ── main ── */
export default function Dashboard() {
  const [state, setState] = useState({ loading: true, error: null, data: null })

  async function load() {
    setState(s => ({ ...s, loading: true, error: null }))
    try {
      const results = await Promise.allSettled([
        api.get('/alunos'),
        api.get('/turmas'),
        api.get('/matriculas'),
        api.get('/notas'),
        api.get('/mensalidades'),
        api.get('/frequencias'),
        api.get('/comunicados'),
      ])
      const [alunos, turmas, matriculas, notas, mensalidades, frequencias, comunicados] = results.map(r =>
        r.status === 'fulfilled' ? r.value : []
      )
      setState({ loading: false, error: null, data: { alunos, turmas, matriculas, notas, mensalidades, frequencias, comunicados } })
    } catch (e) {
      setState({ loading: false, error: e.message, data: null })
    }
  }

  useEffect(() => { load() }, [])

  const { loading, error, data } = state

  if (loading) return <Skeleton />
  if (error) return (
    <div className="card" style={{ padding: 40, textAlign: 'center', color: 'var(--danger)' }}>
      Erro ao carregar dashboard: {error}
      <br /><button className="btn btn-secondary" style={{ marginTop: 12 }} onClick={load}>Tentar novamente</button>
    </div>
  )

  const { alunos, turmas, matriculas, notas, mensalidades, frequencias, comunicados } = data

  /* ── compute stats ── */
  const alunosAtivos = alunos.filter(a => a.ativo).length

  const mediaGeral = avg(notas.map(n => n.valor))

  const totalFreq = frequencias.length
  const freqMedia = totalFreq ? Math.round(frequencias.filter(f => f.presente).length / totalFreq * 100) : null

  const mPago     = mensalidades.filter(m => m.status === 'pago').length
  const mPendente = mensalidades.filter(m => m.status === 'pendente').length
  const mAtrasado = mensalidades.filter(m => m.status === 'atrasado').length
  const mTotal    = mensalidades.length || 1
  const valorRecebido = mensalidades.filter(m => m.status === 'pago').reduce((s, m) => s + Number(m.valor), 0)
  const inadimplencia = mTotal > 1 ? Math.round((mAtrasado / mTotal) * 100) : 0

  /* ── performance by turma ── */
  const turmaPerf = turmas.map(t => {
    const alunoIds = matriculas.filter(m => m.turma_id === t.id).map(m => m.aluno_id)
    const turmaNotas = notas.filter(n => alunoIds.includes(n.aluno_id))
    const media = avg(turmaNotas.map(n => n.valor))
    const turmaFreqs = frequencias.filter(f => alunoIds.includes(f.aluno_id))
    const freq = turmaFreqs.length ? Math.round(turmaFreqs.filter(f => f.presente).length / turmaFreqs.length * 100) : null
    return { nome: t.nome, media, freq }
  }).sort((a, b) => (b.media ?? 0) - (a.media ?? 0))

  const maxMedia = Math.max(...turmaPerf.map(t => t.media ?? 0), 10)

  /* ── alunos em atenção ── */
  const alunosAtencao = alunos.map(aluno => {
    const aNs = notas.filter(n => n.aluno_id === aluno.id)
    const media = avg(aNs.map(n => n.valor))
    const aFs = frequencias.filter(f => f.aluno_id === aluno.id)
    const freq = aFs.length ? Math.round(aFs.filter(f => f.presente).length / aFs.length * 100) : null
    return { ...aluno, media, freq }
  }).filter(a => (a.media !== null && a.media < 6) || (a.freq !== null && a.freq < 75))
    .sort((a, b) => (a.media ?? 10) - (b.media ?? 10))
    .slice(0, 6)

  /* ── comunicados recentes ── */
  const recentesComunicados = [...comunicados]
    .sort((a, b) => (b.enviado_em ?? '').localeCompare(a.enviado_em ?? ''))
    .slice(0, 5)

  /* ── render ── */
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>

      {/* ── stat cards ── */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
        <StatCard label="Alunos Ativos" value={alunosAtivos} sub={`de ${alunos.length} cadastrados`} color="#1d6fbd" icon="🎓" />
        <StatCard label="Média Geral" value={fmt(mediaGeral)} sub="todas as disciplinas" color="#f59e0b" icon="📊" />
        <StatCard label="Frequência Média" value={freqMedia !== null ? freqMedia + '%' : '—'} sub="presença nas aulas" color="#10b981" icon="📋" />
        <StatCard label="Inadimplência" value={inadimplencia + '%'} sub={`${mAtrasado} mensalidade${mAtrasado !== 1 ? 's' : ''} atrasada${mAtrasado !== 1 ? 's' : ''}`} color="#ef4444" icon="⚠️" />
      </div>

      {/* ── charts row ── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>

        {/* Desempenho por turma */}
        <div className="card">
          <SectionTitle>Desempenho por Turma</SectionTitle>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            {turmaPerf.map(t => (
              <div key={t.nome}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                  <span style={{ fontSize: 13, fontWeight: 500 }}>{t.nome}</span>
                  <span style={{
                    fontSize: 13, fontWeight: 700, color: notaClass(t.media),
                    background: notaClass(t.media) + '15', padding: '2px 10px', borderRadius: 20,
                  }}>{fmt(t.media)}</span>
                </div>
                <Bar value={t.media ?? 0} max={10} color={notaClass(t.media)} />
              </div>
            ))}
          </div>
        </div>

        {/* Situação financeira */}
        <div className="card">
          <SectionTitle>Situação Financeira — 2025</SectionTitle>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginBottom: 24 }}>
            {[
              { label: 'Pagas', count: mPago, color: '#10b981', bg: '#ecfdf5' },
              { label: 'Pendentes', count: mPendente, color: '#f59e0b', bg: '#fffbeb' },
              { label: 'Atrasadas', count: mAtrasado, color: '#ef4444', bg: '#fef2f2' },
            ].map(({ label, count, color, bg }) => (
              <div key={label}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{ width: 10, height: 10, borderRadius: '50%', background: color, display: 'inline-block' }} />
                    <span style={{ fontSize: 13 }}>{label}</span>
                  </div>
                  <span style={{
                    fontSize: 13, fontWeight: 700, color,
                    background: bg, padding: '2px 10px', borderRadius: 20,
                  }}>{count}</span>
                </div>
                <Bar value={count} max={mTotal} color={color} />
              </div>
            ))}
          </div>

          <div style={{
            background: 'var(--surface-2)', borderRadius: 10, padding: '14px 16px',
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          }}>
            <span style={{ fontSize: 12, color: 'var(--text-2)', fontWeight: 500 }}>Valor arrecadado no ano</span>
            <span style={{ fontSize: 18, fontWeight: 700, color: '#059669' }}>{fmtBRL(valorRecebido)}</span>
          </div>
        </div>
      </div>

      {/* ── bottom row ── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>

        {/* Alunos em atenção */}
        <div className="card">
          <SectionTitle>Alunos que Precisam de Atenção</SectionTitle>
          {alunosAtencao.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '24px 0', color: 'var(--text-3)', fontSize: 13 }}>
              Nenhum aluno em situação crítica
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {alunosAtencao.map(a => (
                <div key={a.id} style={{
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  padding: '10px 12px', background: 'var(--surface-2)', borderRadius: 8,
                  borderLeft: '3px solid ' + (a.media !== null && a.media < 6 ? 'var(--danger)' : 'var(--warning)'),
                }}>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: 13 }}>{a.nome}</div>
                    <div style={{ fontSize: 11, color: 'var(--text-3)', marginTop: 2 }}>
                      {a.freq !== null && a.freq < 75 ? `Frequência: ${a.freq}%` : ''}
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    {a.media !== null && (
                      <span style={{
                        fontSize: 14, fontWeight: 700,
                        color: a.media < 6 ? 'var(--danger)' : 'var(--warning)',
                      }}>
                        {fmt(a.media)}
                      </span>
                    )}
                    {a.freq !== null && a.freq < 75 && (
                      <div style={{ fontSize: 11, color: 'var(--warning)', marginTop: 2 }}>{a.freq}% presença</div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Comunicados recentes */}
        <div className="card">
          <SectionTitle>Comunicados Recentes</SectionTitle>
          {recentesComunicados.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '24px 0', color: 'var(--text-3)', fontSize: 13 }}>Nenhum comunicado.</div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {recentesComunicados.map(c => (
                <div key={c.id} style={{
                  padding: '10px 12px', background: 'var(--surface-2)', borderRadius: 8,
                  borderLeft: '3px solid var(--primary)',
                }}>
                  <div style={{ fontWeight: 600, fontSize: 13, color: 'var(--text)' }}>{c.titulo}</div>
                  <div style={{ fontSize: 11, color: 'var(--text-3)', marginTop: 3 }}>
                    {c.enviado_em ? new Date(c.enviado_em).toLocaleDateString('pt-BR') : ''}
                    {c.ativo ? '' : ' · Arquivado'}
                  </div>
                  <div style={{ fontSize: 12, color: 'var(--text-2)', marginTop: 4,
                    overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '100%' }}>
                    {c.conteudo}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

    </div>
  )
}
