import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'
import { ToastProvider } from './components/Toast'
import Alunos from './pages/Alunos'
import Turmas from './pages/Turmas'
import Boletim from './pages/Boletim'
import Financeiro from './pages/Financeiro'
import Comunicados from './pages/Comunicados'
import Usuarios from './pages/Usuarios'

const PAGES = {
  alunos:      { title: 'Alunos & Matrículas',    component: Alunos      },
  turmas:      { title: 'Turmas & Disciplinas',    component: Turmas      },
  boletim:     { title: 'Boletim & Frequência',    component: Boletim     },
  financeiro:  { title: 'Financeiro',              component: Financeiro  },
  comunicados: { title: 'Comunicados',             component: Comunicados },
  usuarios:    { title: 'Usuários',                component: Usuarios    },
}

export default function App() {
  const [current, setCurrent] = useState('alunos')
  const Page = PAGES[current]?.component

  return (
    <ToastProvider>
      <div className="layout">
        <Sidebar current={current} onNavigate={setCurrent} />
        <div className="main">
          <Topbar title={PAGES[current]?.title} />
          <div className="content">
            {Page && <Page key={current} />}
          </div>
        </div>
      </div>
    </ToastProvider>
  )
}
