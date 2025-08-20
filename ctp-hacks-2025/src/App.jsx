import { useState } from 'react'
import './App.css'

function App() {
  const [image, setImage] = useState(null)

  // handle image selection
  const handleImageUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      const imageUrl = URL.createObjectURL(file)
      setImage(imageUrl)
    }
  }

  return (
    <>
      <h2>Please upload an image</h2>
      <div className="card">
        {/* File input */}
        <input 
          type="file" 
          accept="image/*" 
          onChange={handleImageUpload} 
        />

        {/* Display the uploaded image */}
        {image && (
          <div style={{ marginTop: '20px' }}>
            <img 
              src={image} 
              alt="Uploaded" 
              style={{ maxWidth: '100%', maxHeight: '400px', borderRadius: '8px' }}
            />
          </div>
        )}
      </div>
    </>
  )
}

export default App
