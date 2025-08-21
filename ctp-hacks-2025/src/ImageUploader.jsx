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

  // // step 1: make function
  // async function generatePlaylist(files) {
  //   console.log('Generating playlist for files:', files)
  //   const uploadPromises = files.map(file => {
  //     console.log('File type:', file)
  //     const formData = new FormData()
  //     formData.append('filedata', file)
  //     // const data = {
  //     //   // filename: index,
  //     //   filedata: file
  //     // }

  //     return fetch('http://localhost:8000/', {
  //       method: 'POST',
  //       body: JSON.stringify(formData)
  //     })
  //       .then(response => response.json())
  //       .then(data => {
  //         console.log('File uploaded successfully:', data)
  //         return data
  //       })
  //       .catch(error => {
  //         console.error('Error uploading file:', error)
  //       })
  //   })

  //   const results = await Promise.all(uploadPromises)
  //   console.log('All files processed:', results)

  //   return (
  //     <div>
  //       <h3>Generated Playlists</h3>
  //       <ul>
  //         {results.map((result, index) => (
  //           <li key={index}>{result}</li>
  //         ))}
  //       </ul>
  //     </div>
  //   )



  // }

  // remove a single image
  function handleRemoveImage(index) {
    const updatedImages = images.filter((_, i) => i !== index)
    setImages(updatedImages)
    sessionStorage.setItem('uploadedImages', JSON.stringify(updatedImages))
  }

  // step 2: add it to the component
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
            <br />
            <button onClick={() => handleRemoveImage(index)} style={{ marginTop: '5px' }}>
              Remove
            </button>
            {/* <button onClick={() => generatePlaylist(images)} style={{ marginLeft: '10px' }}>
              Generate Playlist
            </button> */}
          </div>
        ))}
      </div>
    </div>
  )
}

export default ImageUploader
