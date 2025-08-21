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

  // remove all images
  const handleRemoveAllImages = () => {
    setImages([]);
  };

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
    </div>
  </div>
);
}

export default ImageUploader
