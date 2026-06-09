import { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'
import { ToastProvider } from './components/Toast'
import Alunos from './pages/Alunos'
import Turmas from './pages/Turmas'
import Boletim from './pages/Boletim'
import Financeiro from './pages/Financeiro'
import Comunicados from './pages/Comunicados'
import Usuarios from './pages/Usuarios'
import Login from './pages/Login'
import { setToken } from './api/client'

const PAGES = {
  alunos:      { title: 'Alunos & Matrículas',    component: Alunos      },
  turmas:      { title: 'Turmas & Disciplinas',    component: Turmas      },
  boletim:     { title: 'Boletim & Frequência',    component: Boletim     },
  financeiro:  { title: 'Financeiro',              component: Financeiro  },
  comunicados: { title: 'Comunicados',             component: Comunicados },
  usuarios:    { title: 'Usuários',                component: Usuarios    },
}

export default function App() {
  const [authed, setAuthed] = useState(!!localStorage.getItem('token'))
  const [current, setCurrent] = useState('alunos')

  useEffect(() => {
    function onLogout() { setAuthed(false) }
    window.addEventListener('auth:logout', onLogout)
    return () => window.removeEventListener('auth:logout', onLogout)
  }, [])

  function handleLogin() { setAuthed(true) }
  function handleLogout() { setToken(null); setAuthed(false) }

  if (!authed) return <Login onLogin={handleLogin} />

  const Page = PAGES[current]?.component
  return (
    <ToastProvider>
      <div className="layout">
        <Sidebar current={current} onNavigate={setCurrent} />
        <div className="main">
          <Topbar title={PAGES[current]?.title} onLogout={handleLogout} />
          <div className="content">
            {Page && <Page key={current} />}
          </div>
        </div>
      </div>
    </ToastProvider>
  )
}
