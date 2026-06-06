export function Loading({ rows = 5 }) {
  return (
    <tbody>
      {Array.from({ length: rows }).map((_, i) => (
        <tr key={i} className="skeleton-row">
          {Array.from({ length: 5 }).map((_, j) => (
            <td key={j}>
              <span className="skeleton skeleton-cell" style={{ width: `${60 + Math.random() * 30}%` }} />
            </td>
          ))}
        </tr>
      ))}
    </tbody>
  )
}

export function Empty({ title = 'Nenhum registro', desc, action }) {
  return (
    <div className="state-box">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 9h6M9 13h4"/>
      </svg>
      <p><strong>{title}</strong>{desc && desc}</p>
      {action}
    </div>
  )
}

export function ErrorBox({ message, onRetry }) {
  return (
    <div className="state-box">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#dc2626" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <p><strong>Erro ao carregar</strong>{message}</p>
      {onRetry && <button className="btn btn-secondary" onClick={onRetry}>Tentar novamente</button>}
    </div>
  )
}

export function Badge({ status }) {
  const map = {
    ativa:    { cls: 'badge-success', label: 'Ativa'     },
    trancada: { cls: 'badge-warning', label: 'Trancada'  },
    cancelada:{ cls: 'badge-danger',  label: 'Cancelada' },
    pago:     { cls: 'badge-success', label: 'Pago'      },
    pendente: { cls: 'badge-neutral', label: 'Pendente'  },
    atrasado: { cls: 'badge-danger',  label: 'Atrasado'  },
    ativo:    { cls: 'badge-success', label: 'Ativo'     },
    inativo:  { cls: 'badge-neutral', label: 'Inativo'   },
    true:     { cls: 'badge-success', label: 'Ativo'     },
    false:    { cls: 'badge-neutral', label: 'Inativo'   },
  }
  const v = map[String(status)] || { cls: 'badge-neutral', label: String(status) }
  return <span className={`badge ${v.cls}`}>{v.label}</span>
}
