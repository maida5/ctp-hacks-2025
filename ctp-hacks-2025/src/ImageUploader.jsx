import React, { useState, useEffect } from 'react'

function ImageUploader() {
  const [images, setImages] = useState([])
  const [suggestions, setSuggestions] = useState("") 
  const [loading, setLoading] = useState(false)

  // load upload images from sessionStorage
  useEffect(() => {
    const savedImages = sessionStorage.getItem('uploadedImages')
    if (savedImages) {
      setImages(JSON.parse(savedImages))
    }
  }, [])

  // handle multiple image uploads
  function handleImageUpload(event) {
    const files = Array.from(event.target.files)
    files.forEach(file => {
      const reader = new FileReader()
      reader.onload = () => {
        const base64 = reader.result
        setImages(prevImages => {
          const updatedImages = [...prevImages, base64]
          sessionStorage.setItem('uploadedImages', JSON.stringify(updatedImages))
          return updatedImages
        })
      }
      reader.readAsDataURL(file)
    })
  }

  // remove a single image
  // function handleRemoveImage(index) {
  //   const updatedImages = images.filter((_, i) => i !== index)
  //   setImages(updatedImages)
  //   sessionStorage.setItem('uploadedImages', JSON.stringify(updatedImages))
  // }

  const handleRemoveAllImages = () => {
    setImages([]); // This clears the entire array, removing all images
    sessionStorage.removeItem('uploadedImages') 
    setSuggestions("")                           
    setLoading(false)    
  };
async function analyzeImage() {
    if (images.length === 0) return
    setLoading(true)
    setSuggestions("")

    try {
      // Take first image (data URL / base64)
      const base64 = images[0]
      const mimeMatch = base64.match(/^data:(.+);base64,/)
      const mime = (mimeMatch && mimeMatch[1]) ? mimeMatch[1] : "image/png"

      // Convert base64 → File
      const clean = base64.includes(",") ? base64.split(",")[1] : base64
      const byteString = atob(clean)
      const ab = new ArrayBuffer(byteString.length)
      const ia = new Uint8Array(ab)
      for (let i = 0; i < byteString.length; i++) ia[i] = byteString.charCodeAt(i)
      const file = new File([ab], "upload.png", { type: mime })

      // Send as multipart/form-data to FastAPI
      const form = new FormData()
      form.append("file", file)

      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: form,
      })

      if (!res.ok) {
        const text = await res.text()
        throw new Error(text || `HTTP ${res.status}`)
      }

      const data = await res.json() // { filename, suggestions_text }
      setSuggestions(data.suggestions_text || "No suggestions returned")
    } catch (err) {
      setSuggestions("Error: " + (err?.message || String(err)))
    } finally {
      setLoading(false)
    }
  }

return (
  <div style={{ textAlign: 'center', marginTop: '20px' }}>
    <input
      type="file"
      id="file-upload"
      accept="image/*"
      multiple
      onChange={handleImageUpload}
      style={{ display: 'none' }}
    />
    
    <label 
      htmlFor="file-upload" 
      style={{
        padding: '10px 20px',
        backgroundColor: '#7E4E4E',
        color: 'white',
        borderRadius: '5px',
        cursor: 'pointer',
        border: 'none',
        fontSize: '16px',
        transition: 'background-color 0.3s ease',
      }}
      onMouseEnter={(e) => { e.target.style.backgroundColor = '#653E3E'; }}
      onMouseLeave={(e) => { e.target.style.backgroundColor = '#7E4E4E'; }}
    >
      Choose Files
    </label>

{images.length > 0 && (
        <button
          onClick={analyzeImage}
          disabled={loading}
          style={{
            marginLeft: 10,
            padding: '10px 20px',
            backgroundColor: '#2d6cdf',
            color: '#fff',
            borderRadius: 5,
            border: 'none',
            cursor: 'pointer',
            transition: 'background-color 0.3s ease',
          }}
          onMouseEnter={(e) => { e.target.style.backgroundColor = '#2257b7'; }}
          onMouseLeave={(e) => { e.target.style.backgroundColor = '#2d6cdf'; }}
        >
          {loading ? 'Analyzing...' : 'Analyze First Image'}
        </button>
      )}

    <div style={{ marginTop: '20px' }}>
      {/* Display a "Remove All" button only if there are images */}
      {images.length > 0 && (
        <button 
          onClick={handleRemoveAllImages} 
          style={{ 
            marginTop: '10px', 
            marginBottom: '20px', 
            backgroundColor: '#7E4E4E',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            borderRadius: '5px',
            cursor: 'pointer',
            transition: 'background-color 0.3s ease',
          }}
          onMouseEnter={(e) => { e.target.style.backgroundColor = '#653E3E'; }}
          onMouseLeave={(e) => { e.target.style.backgroundColor = '#7E4E4E'; }}
        >
          Remove All Images
        </button>
      )}

      {/* The rest of the image display logic */}
      {images.map((image, index) => (
        <div key={index} style={{ marginBottom: '10px' }}>
          <img
            src={image}
            alt={`Uploaded ${index}`}
            style={{ maxWidth: '100%', maxHeight: '400px', borderRadius: '4px' }}
          />
        </div>
      ))}
      {suggestions && (
          <pre style={{ whiteSpace: 'pre-wrap', textAlign: 'left', marginTop: 12 }}>
            {suggestions}
          </pre>
        )}
    </div>
  </div>
);
}

export default ImageUploader
