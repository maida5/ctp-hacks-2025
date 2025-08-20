import React, { useState, useEffect } from 'react'

function ImageUploader() {
  const [images, setImages] = useState([])

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
  function handleRemoveImage(index) {
    const updatedImages = images.filter((_, i) => i !== index)
    setImages(updatedImages)
    sessionStorage.setItem('uploadedImages', JSON.stringify(updatedImages))
  }

  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <input type="file" accept="image/*" multiple onChange={handleImageUpload} />
      <div style={{ marginTop: '20px' }}>
        {images.map((image, index) => (
          <div key={index} style={{ marginBottom: '10px' }}>
            <img
              src={image}
              alt={`Uploaded ${index}`}
              style={{ maxWidth: '100%', maxHeight: '400px', borderRadius: '4px' }}
            />
            <br/>
            <button onClick={() => handleRemoveImage(index)} style={{ marginTop: '5px' }}>
              Remove
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ImageUploader
