import React, { useState, useEffect, useRef } from 'react';

function ImageUploader() {
  const [images, setImages] = useState([]);
  const [isHovering, setIsHovering] = useState(false); // Make sure this line is present
  const fileInputRef = useRef(null); 

  // load upload images from sessionStorage
  useEffect(() => {
    const savedImages = sessionStorage.getItem('uploadedImages');
    if (savedImages) {
      setImages(JSON.parse(savedImages));
    }
  }, []);

  // handle multiple image uploads
  function handleImageUpload(event) {
    const files = Array.from(event.target.files);
    files.forEach(file => {
      const reader = new FileReader();
      reader.onload = () => {
        const base64 = reader.result;
        setImages(prevImages => {
          const updatedImages = [...prevImages, base64];
          sessionStorage.setItem('uploadedImages', JSON.stringify(updatedImages));
          return updatedImages;
        });
      };
      reader.readAsDataURL(file);
    });
  }

  // remove all images
  const handleRemoveAllImages = () => {
    setImages([]);
    sessionStorage.removeItem('uploadedImages');
  };

  // Define button colors
  const buttonColor = isHovering ? '#e0e1dd' : '#fefae0';

  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <input
        type="file"
        ref={fileInputRef} 
        accept="image/*"
        multiple
        onChange={handleImageUpload}
        style={{ display: 'none' }}
      />
      
      {/* Use state to manage the style */}
      <button 
        onClick={() => fileInputRef.current.click()}
        onMouseEnter={() => setIsHovering(true)}
        onMouseLeave={() => setIsHovering(false)}
        style={{
          padding: '10px 20px',
          backgroundColor: buttonColor, // Use the state-driven color
          color: 'black',
          borderRadius: '5px',
          cursor: 'pointer',
          border: 'none',
          fontSize: '16px',
          transition: 'background-color 0.3s ease',
          fontFamily: 'Red Hat Text, sans-serif'
        }}
      >
        Choose Files
      </button>

      <div style={{ marginTop: '20px' }}>
        {images.length > 0 && (
          <button 
            onClick={handleRemoveAllImages} 
            style={{ 
              marginTop: '10px', 
              marginBottom: '20px', 
              backgroundColor: '#fefae0',
              color: 'black',
              border: 'none',
              padding: '10px 20px',
              borderRadius: '5px',
              cursor: 'pointer',
              transition: 'background-color 0.3s ease',
              fontFamily: 'Delius Swash Caps, cursive'
            }}
            onMouseEnter={(e) => { e.target.style.backgroundColor = '#e0e1dd'; }}
            onMouseLeave={(e) => { e.target.style.backgroundColor = '#fefae0'; }}
          >
            Remove All Images
          </button>
        )}

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

export default ImageUploader;