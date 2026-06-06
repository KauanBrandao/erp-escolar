export default function Topbar({ title, actions }) {
  return (
    <header className="topbar">
      <span className="topbar-title">{title}</span>
      {actions && <div className="topbar-right">{actions}</div>}
    </header>
  )
}
