import { useState, useEffect } from 'react'

const ImageUploader = () => {
  const [image, setImage] = useState(null)

  // load saved image from sessionStorage
  useEffect(() => {
    const savedImage = sessionStorage.getItem('uploadedImage')
    if (savedImage) {
      setImage(savedImage)
    }
  }, [])

  // handle image upload
  const handleImageUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = () => {
        const base64 = reader.result
        setImage(base64)
        sessionStorage.setItem('uploadedImage', base64)
      }
      reader.readAsDataURL(file)
    }
  }

  // remove image from sessionStorage
  const handleRemoveImage = () => {
    setImage(null)
    sessionStorage.removeItem('uploadedImage')
  }

  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <input 
        type="file" 
        accept="image/*" 
        onChange={handleImageUpload} 
      />
      {image && (
        <div style={{ marginTop: '20px' }}>
          <img 
            src={image} 
            alt="Uploaded" 
            style={{ maxWidth: '100%', maxHeight: '400px', borderRadius: '8px' }}
          />
          <br />
          <button onClick={handleRemoveImage} style={{ marginTop: '10px' }}>
            Remove Image
          </button>
        </div>
      )}
    </div>
  )
}

export default ImageUploader
