export default function Topbar({ title, actions, onLogout }) {
  return (
    <header className="topbar">
      <span className="topbar-title">{title}</span>
      <div className="topbar-right">
        {actions}
        {onLogout && (
          <button className="btn btn-secondary btn-sm" onClick={onLogout} style={{ marginLeft: '8px' }}>
            Sair
          </button>
        )}
      </div>
    </header>
  )
}
