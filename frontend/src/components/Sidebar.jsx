const NAV = [
  {
    section: 'Acadêmico',
    items: [
      {
        id: 'alunos',
        label: 'Alunos & Matrículas',
        icon: (
          <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
        ),
      },
      {
        id: 'turmas',
        label: 'Turmas & Disciplinas',
        icon: (
          <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
            <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
          </svg>
        ),
      },
      {
        id: 'boletim',
        label: 'Boletim & Frequência',
        icon: (
          <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10 9 9 9 8 9"/>
          </svg>
        ),
      },
    ],
  },
  {
    section: 'Financeiro & Gestão',
    items: [
      {
        id: 'financeiro',
        label: 'Financeiro',
        icon: (
          <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="1" x2="12" y2="23"/>
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
          </svg>
        ),
      },
      {
        id: 'comunicados',
        label: 'Comunicados',
        icon: (
          <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
        ),
      },
      {
        id: 'usuarios',
        label: 'Usuários',
        icon: (
          <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
        ),
      },
    ],
  },
]

export default function Sidebar({ current, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-mark">E</div>
        <div className="sidebar-logo-text">
          <span className="sidebar-logo-name">ERP Escolar</span>
          <span className="sidebar-logo-sub">Gestão Educacional</span>
        </div>
      </div>

      <nav style={{ flex: 1, overflowY: 'auto', padding: '8px 0' }}>
        {NAV.map(section => (
          <div key={section.section} className="sidebar-section">
            <div className="sidebar-section-label">{section.section}</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
              {section.items.map(item => (
                <button
                  key={item.id}
                  className={`nav-item${current === item.id ? ' active' : ''}`}
                  onClick={() => onNavigate(item.id)}
                >
                  {item.icon}
                  {item.label}
                </button>
              ))}
            </div>
          </div>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-user">
          <div className="user-avatar">A</div>
          <div className="user-info">
            <div className="user-name">Administrador</div>
            <div className="user-role">admin@escola.com</div>
          </div>
        </div>
      </div>
    </aside>
  )
}
