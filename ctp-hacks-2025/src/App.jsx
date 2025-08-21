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
    </>
  )
}

export default App
