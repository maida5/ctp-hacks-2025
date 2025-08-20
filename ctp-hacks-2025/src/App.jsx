import './App.css'
import ImageUploader from './ImageUploader'

function App() {
  return (
    <>
      <h1>SOME TITLE</h1>
      <h2>Please upload an image</h2>
      <div className="card">
        <ImageUploader />
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <ApiHello />
    </>
  )
}

function ApiHello() {
  console.log('Starting to render APIHELLO')
  const [message, setMessage] = useState('')

  const fetchMessage = async () => {
    const res = await fetch('https://ctp-hacks-2025.vercel.app/hello', {
        // mode: 'no-cors',
        method: 'GET'
        // headers: {'Access- Control-Allow-Origin': '*'
        }
    )
    console.log('ERROR 1?')
    const data = await res.json()
    console.log('ERROR 2?')
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
