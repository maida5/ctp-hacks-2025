import './App.css'
import ImageUploader from './ImageUploader'

// function App() {
//   return (
//     <>
//       <h1>SOME TITLE</h1>
//       <h2>Please upload an image</h2>
//       <div className="card">
//         <ImageUploader />
//       </div>
//       <p className="read-the-docs">
//         Click on the Vite and React logos to learn more
//       </p>
//     </>
//   )
// }

function App() {
  return (
    // Wrap your entire content in the div with the new class
    <div className="animated-background">
      {/* All your original content goes here */}
      <h1>SOME TITLE</h1>
      <h2>Please upload an image</h2>
      <div className="card">
        <ImageUploader />
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </div>
  )
}

export default App