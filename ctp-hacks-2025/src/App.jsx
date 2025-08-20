import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <ApiHello />
    </>
  )
}

function ApiHello() {
  const [message, setMessage] = useState('')

  const fetchMessage = async () => {
    const res = await fetch('https://ctp-hacks-2025-maida5s-projects.vercel.app/', {
        headers: {'Access-Control-Allow-Origin': '*'}
      }
    )
    const data = await res.json()
    setMessage(data.message)
  }

  return (
    <div>
      <button onClick={fetchMessage}>Get API Message</button>
      <div>{message}</div>
    </div>
  )
}

export default App
