import { useState, useEffect, useRef } from 'react'
import { api } from '../api/client'

/* ── inject keyframes once ───────────────────────────────── */
const STYLE = `
@keyframes dash-fade-up {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: none; }
}
@keyframes dash-bar-fill {
  from { width: 0 !important; }
}
`
if (!document.getElementById('dash-style')) {
  const s = document.createElement('style')
  s.id = 'dash-style'
  s.textContent = STYLE
  document.head.appendChild(s)
}

/* ── helpers ─────────────────────────────────────────────── */
const avg = arr => arr.length ? arr.reduce((s, n) => s + Number(n), 0) / arr.length : null
const fmt1 = v => v == null ? '—' : Number(v).toFixed(1)
const fmtBRL = v => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })

function gradeColor(v) {
  if (v == null) return '#94a3b8'
  if (v >= 7)   return '#059669'
  if (v >= 5)   return '#d97706'
  return '#dc2626'
}

function today() {
  return new Date().toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
}

/* ── icon components ────────────────────────────────────── */
function IconStudents() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
      <circle cx="9" cy="7" r="4"/>
      <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
      <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
    </svg>
  )
}
function IconChart() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="20" x2="18" y2="10"/>
      <line x1="12" y1="20" x2="12" y2="4"/>
      <line x1="6"  y1="20" x2="6"  y2="14"/>
      <line x1="2"  y1="20" x2="22" y2="20"/>
    </svg>
  )
}
function IconClock() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/>
      <polyline points="12 6 12 12 16 14"/>
    </svg>
  )
}
function IconAlert() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
      <line x1="12" y1="9" x2="12" y2="13"/>
      <line x1="12" y1="17" x2="12.01" y2="17"/>
    </svg>
  )
}

/* ── KPI card ────────────────────────────────────────────── */
function KpiCard({ label, value, sub, icon, iconColor, iconBg, delay }) {
  return (
    <div
      className="card"
      style={{
        padding: '20px 22px',
        display: 'flex',
        alignItems: 'flex-start',
        gap: 14,
        animation: `dash-fade-up 0.45s ease both`,
        animationDelay: delay,
        borderTop: `3px solid ${iconColor}`,
      }}
    >
      <div style={{
        width: 42, height: 42, borderRadius: 10, background: iconBg,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        color: iconColor, flexShrink: 0,
      }}>
        {icon}
      </div>
      <div style={{ minWidth: 0, flex: 1 }}>
        <div style={{ fontSize: 28, fontWeight: 700, lineHeight: 1, color: 'var(--text)', fontFamily: 'Syne, sans-serif' }}>
          {value}
        </div>
        <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text)', marginTop: 5 }}>{label}</div>
        <div style={{ fontSize: 11, color: 'var(--text-3)', marginTop: 2, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{sub}</div>
      </div>
    </div>
  )
}

/* ── animated bar ────────────────────────────────────────── */
function AnimBar({ pct, color, animate }) {
  return (
    <div style={{ background: 'var(--border)', borderRadius: 6, height: 8, overflow: 'hidden' }}>
      <div style={{
        height: '100%',
        width: animate ? `${Math.min(pct, 100)}%` : '0%',
        background: color,
        borderRadius: 6,
        transition: 'width 0.8s cubic-bezier(0.4,0,0.2,1)',
      }} />
    </div>
  )
}

/* ── section heading ─────────────────────────────────────── */
function SectionHead({ children }) {
  return (
    <div style={{
      fontFamily: 'Syne, sans-serif',
      fontSize: 13, fontWeight: 700,
      color: 'var(--text-2)',
      textTransform: 'uppercase',
      letterSpacing: '0.07em',
      marginBottom: 18,
    }}>
      {children}
    </div>
  )
}

/* ── skeleton ────────────────────────────────────────────── */
function Pulse({ h = 100 }) {
  return (
    <div className="card" style={{ height: h, background: 'linear-gradient(90deg,var(--surface-2) 25%,var(--border) 50%,var(--surface-2) 75%)', backgroundSize: '200%', animation: 'none' }} />
  )
}
function DashSkeleton() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, minmax(0,1fr))', gap: 16 }}>
        {[0,1,2,3].map(i => <Pulse key={i} h={110} />)}
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0,3fr) minmax(0,2fr)', gap: 16 }}>
        <Pulse h={300} />
        <Pulse h={300} />
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0,1fr) minmax(0,1fr)', gap: 16 }}>
        <Pulse h={220} />
        <Pulse h={220} />
      </div>
    </div>
  )
}

/* ══════════════════════════════════════════════════════════ */
export default function Dashboard() {
  const [status, setStatus] = useState('loading') // loading | error | ok
  const [data, setData]     = useState(null)
  const [err, setErr]       = useState(null)
  const [animated, setAnimated] = useState(false)

  async function load() {
    setStatus('loading')
    try {
      const settled = await Promise.allSettled([
        api.get('/alunos'),
        api.get('/turmas'),
        api.get('/matriculas'),
        api.get('/notas'),
        api.get('/mensalidades'),
        api.get('/frequencias'),
        api.get('/comunicados'),
        api.get('/pagamentos'),
      ])
      const [alunos, turmas, matriculas, notas, mensalidades, frequencias, comunicados, pagamentos] =
        settled.map(r => r.status === 'fulfilled' ? r.value : [])
      setData({ alunos, turmas, matriculas, notas, mensalidades, frequencias, comunicados, pagamentos })
      setStatus('ok')
      setTimeout(() => setAnimated(true), 80)
    } catch (e) {
      setErr(e.message)
      setStatus('error')
    }
  }

  useEffect(() => { load() }, [])

  if (status === 'loading') return <DashSkeleton />
  if (status === 'error') return (
    <div className="card" style={{ padding: 40, textAlign: 'center' }}>
      <div style={{ color: 'var(--danger)', marginBottom: 12 }}>Erro: {err}</div>
      <button className="btn btn-secondary" onClick={load}>Tentar novamente</button>
    </div>
  )

  const { alunos, turmas, matriculas, notas, mensalidades, frequencias, comunicados, pagamentos } = data

  /* ── compute ── */
  const anoAtual = new Date().getFullYear()

  function getMensStatus(mens) {
    const pag = pagamentos.find(p => p.mensalidade_id === mens.id)
    if (pag) return 'pago'
    const venc = new Date(mens.vencimento)
    if (venc < new Date()) return 'atrasado'
    return 'pendente'
  }

  const alunosAtivos  = alunos.filter(a => a.ativo).length
  const mediaGeral    = avg(notas.map(n => n.valor))
  const freqTotal     = frequencias.length
  const freqMedia     = freqTotal ? Math.round(frequencias.filter(f => f.presente).length / freqTotal * 100) : null

  // Financeiro: só o ano atual
  const mensAnoAtual  = mensalidades.filter(m => m.ano === anoAtual)
  const mPago         = mensAnoAtual.filter(m => getMensStatus(m) === 'pago').length
  const mPendente     = mensAnoAtual.filter(m => getMensStatus(m) === 'pendente').length
  const mAtrasado     = mensAnoAtual.filter(m => getMensStatus(m) === 'atrasado').length
  const mTotal        = mensAnoAtual.length || 1
  const valorRecebido = mensAnoAtual
    .map(m => pagamentos.find(p => p.mensalidade_id === m.id))
    .filter(Boolean)
    .reduce((s, p) => s + Number(p.valor_pago), 0)
  const inadimplencia = Math.round((mAtrasado / mTotal) * 100)

  /* performance por turma */
  const turmaPerf = turmas.map(t => {
    const ids   = matriculas.filter(m => m.turma_id === t.id).map(m => m.aluno_id)
    const tNts  = notas.filter(n => ids.includes(n.aluno_id))
    const tFqs  = frequencias.filter(f => ids.includes(f.aluno_id))
    const media = avg(tNts.map(n => n.valor))
    const freq  = tFqs.length ? Math.round(tFqs.filter(f => f.presente).length / tFqs.length * 100) : null
    return { nome: t.nome, serie: t.serie, media, freq }
  }).sort((a, b) => (b.media ?? 0) - (a.media ?? 0))

  /* alunos em atenção */
  const alunosAtencao = alunos.map(a => {
    const aNts = notas.filter(n => n.aluno_id === a.id)
    const aFqs = frequencias.filter(f => f.aluno_id === a.id)
    const media = avg(aNts.map(n => n.valor))
    const freq  = aFqs.length ? Math.round(aFqs.filter(f => f.presente).length / aFqs.length * 100) : null
    return { ...a, media, freq }
  })
    .filter(a => (a.media != null && a.media < 6) || (a.freq != null && a.freq < 75))
    .sort((a, b) => (a.media ?? 10) - (b.media ?? 10))
    .slice(0, 6)

  /* comunicados recentes */
  const recentes = [...comunicados]
    .sort((a, b) => (b.enviado_em ?? '').localeCompare(a.enviado_em ?? ''))
    .slice(0, 5)

  /* ── render ── */
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>

      {/* header */}
      <div style={{ animation: 'dash-fade-up 0.35s ease both' }}>
        <div style={{ fontSize: 11, color: 'var(--text-3)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 4 }}>
          {today()}
        </div>
        <h1 style={{ fontFamily: 'Syne, sans-serif', fontSize: 22, fontWeight: 700, letterSpacing: '-0.03em', color: 'var(--text)' }}>
          Visão Geral do Sistema
        </h1>
      </div>

      {/* KPI cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, minmax(0,1fr))', gap: 14 }}>
        <KpiCard
          label="Alunos Ativos" value={alunosAtivos}
          sub={`${alunos.length - alunosAtivos} inativo${alunos.length - alunosAtivos !== 1 ? 's' : ''} · ${turmas.length} turmas`}
          icon={<IconStudents />} iconColor="#1d6fbd" iconBg="#dbeafe" delay="0.05s"
        />
        <KpiCard
          label="Média Geral" value={fmt1(mediaGeral)}
          sub="todas as disciplinas e bimestres"
          icon={<IconChart />} iconColor="#d97706" iconBg="#fef3c7" delay="0.12s"
        />
        <KpiCard
          label="Frequência Média" value={freqMedia != null ? freqMedia + '%' : '—'}
          sub={`${frequencias.filter(f => !f.presente).length} faltas registradas`}
          icon={<IconClock />} iconColor="#059669" iconBg="#d1fae5" delay="0.19s"
        />
        <KpiCard
          label="Inadimplência" value={inadimplencia + '%'}
          sub={`${mAtrasado} mensalidade${mAtrasado !== 1 ? 's' : ''} em atraso`}
          icon={<IconAlert />} iconColor="#dc2626" iconBg="#fee2e2" delay="0.26s"
        />
      </div>

      {/* charts row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0,3fr) minmax(0,2fr)', gap: 14 }}>

        {/* desempenho por turma */}
        <div className="card" style={{ padding: '22px 24px', animation: 'dash-fade-up 0.45s ease 0.2s both' }}>
          <SectionHead>Desempenho por Turma</SectionHead>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {turmaPerf.map((t, i) => {
              const color = gradeColor(t.media)
              return (
                <div key={t.nome}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 7 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, minWidth: 0 }}>
                      <span style={{
                        fontSize: 10, fontWeight: 700, color, background: color + '18',
                        padding: '2px 7px', borderRadius: 20, whiteSpace: 'nowrap',
                      }}>
                        {t.serie}
                      </span>
                      <span style={{ fontSize: 13, fontWeight: 500, color: 'var(--text)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {t.nome}
                      </span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexShrink: 0, marginLeft: 10 }}>
                      {t.freq != null && (
                        <span style={{ fontSize: 11, color: t.freq < 75 ? '#d97706' : 'var(--text-3)' }}>
                          {t.freq}% freq.
                        </span>
                      )}
                      <span style={{ fontSize: 14, fontWeight: 700, color, minWidth: 28, textAlign: 'right' }}>
                        {fmt1(t.media)}
                      </span>
                    </div>
                  </div>
                  <AnimBar pct={(t.media ?? 0) / 10 * 100} color={color} animate={animated} />
                </div>
              )
            })}
          </div>
        </div>

        {/* situação financeira */}
        <div className="card" style={{ padding: '22px 24px', animation: 'dash-fade-up 0.45s ease 0.25s both', display: 'flex', flexDirection: 'column', gap: 0 }}>
          <SectionHead>Situação Financeira {anoAtual}</SectionHead>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 16, flex: 1 }}>
            {[
              { label: 'Pagas',     count: mPago,     color: '#059669', bg: '#ecfdf5' },
              { label: 'Pendentes', count: mPendente, color: '#d97706', bg: '#fffbeb' },
              { label: 'Atrasadas', count: mAtrasado, color: '#dc2626', bg: '#fef2f2' },
            ].map(({ label, count, color, bg }) => (
              <div key={label}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 7 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
                    <div style={{ width: 8, height: 8, borderRadius: '50%', background: color, flexShrink: 0 }} />
                    <span style={{ fontSize: 13, color: 'var(--text)' }}>{label}</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{ fontSize: 11, color: 'var(--text-3)' }}>
                      {mTotal > 1 ? Math.round(count / mTotal * 100) : 0}%
                    </span>
                    <span style={{
                      fontSize: 13, fontWeight: 700, color,
                      background: bg, padding: '2px 10px', borderRadius: 20,
                    }}>
                      {count}
                    </span>
                  </div>
                </div>
                <AnimBar pct={count / mTotal * 100} color={color} animate={animated} />
              </div>
            ))}
          </div>

          <div style={{
            marginTop: 20,
            background: 'var(--surface-2)',
            border: '1px solid var(--border)',
            borderRadius: 10,
            padding: '14px 16px',
          }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: 'var(--text-3)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 4 }}>
              Total arrecadado em {anoAtual}
            </div>
            <div style={{ fontSize: 22, fontWeight: 700, color: '#059669', fontFamily: 'Syne, sans-serif', letterSpacing: '-0.02em' }}>
              {fmtBRL(valorRecebido)}
            </div>
            <div style={{ fontSize: 11, color: 'var(--text-3)', marginTop: 2 }}>
              {mPago} parcela{mPago !== 1 ? 's' : ''} confirmada{mPago !== 1 ? 's' : ''}
            </div>
          </div>
        </div>
      </div>

      {/* bottom row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0,1fr) minmax(0,1fr)', gap: 14 }}>

        {/* alunos em atenção */}
        <div className="card" style={{ padding: '22px 24px', animation: 'dash-fade-up 0.45s ease 0.3s both' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 18 }}>
            <SectionHead>Alunos em Atenção</SectionHead>
            {alunosAtencao.length > 0 && (
              <span style={{
                fontSize: 10, fontWeight: 700, color: '#dc2626',
                background: '#fee2e2', padding: '2px 8px', borderRadius: 20, marginBottom: 18,
              }}>
                {alunosAtencao.length} aluno{alunosAtencao.length !== 1 ? 's' : ''}
              </span>
            )}
          </div>
          {alunosAtencao.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '28px 0', color: 'var(--text-3)', fontSize: 13 }}>
              <div style={{ fontSize: 28, marginBottom: 8 }}>✓</div>
              Todos os alunos com desempenho regular
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {alunosAtencao.map(a => {
                const isMedia = a.media != null && a.media < 6
                const isFreq  = a.freq  != null && a.freq  < 75
                const cor     = isMedia ? '#dc2626' : '#d97706'
                return (
                  <div key={a.id} style={{
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    padding: '10px 12px',
                    background: 'var(--surface-2)',
                    border: '1px solid var(--border)',
                    borderLeft: `3px solid ${cor}`,
                    borderRadius: 8, gap: 10,
                  }}>
                    <div style={{ minWidth: 0 }}>
                      <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {a.nome}
                      </div>
                      <div style={{ fontSize: 11, color: 'var(--text-3)', marginTop: 2 }}>
                        {isFreq ? `Frequência: ${a.freq}%` : 'Média abaixo de 6,0'}
                      </div>
                    </div>
                    <div style={{ textAlign: 'right', flexShrink: 0 }}>
                      {a.media != null && (
                        <div style={{ fontSize: 15, fontWeight: 700, color: gradeColor(a.media) }}>
                          {fmt1(a.media)}
                        </div>
                      )}
                      {isFreq && (
                        <div style={{ fontSize: 11, color: '#d97706', fontWeight: 600 }}>{a.freq}%</div>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>

        {/* comunicados recentes */}
        <div className="card" style={{ padding: '22px 24px', animation: 'dash-fade-up 0.45s ease 0.35s both' }}>
          <SectionHead>Comunicados Recentes</SectionHead>
          {recentes.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '28px 0', color: 'var(--text-3)', fontSize: 13 }}>
              Nenhum comunicado cadastrado
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
              {recentes.map((c, i) => (
                <div key={c.id} style={{
                  display: 'flex', gap: 12, alignItems: 'flex-start',
                  padding: '11px 0',
                  borderBottom: i < recentes.length - 1 ? '1px solid var(--border)' : 'none',
                }}>
                  <div style={{
                    width: 6, height: 6, borderRadius: '50%', background: 'var(--primary)',
                    flexShrink: 0, marginTop: 5,
                  }} />
                  <div style={{ minWidth: 0, flex: 1 }}>
                    <div style={{
                      fontSize: 13, fontWeight: 600, color: 'var(--text)',
                      overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                    }}>
                      {c.titulo}
                    </div>
                    <div style={{
                      fontSize: 12, color: 'var(--text-2)', marginTop: 3,
                      overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                    }}>
                      {c.conteudo}
                    </div>
                    <div style={{ fontSize: 10, color: 'var(--text-3)', marginTop: 4, display: 'flex', gap: 8 }}>
                      <span>{c.enviado_em ? new Date(c.enviado_em + 'T00:00:00').toLocaleDateString('pt-BR') : ''}</span>
                      {!c.ativo && <span style={{ color: '#d97706' }}>Arquivado</span>}
                    </div>
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
