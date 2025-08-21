import './App.css'
import React, { useState, useEffect } from 'react'
import ImageUploader from './ImageUploader'

function App() {
  return (
    <div className="animated-background">
      <h1>SOME TITLE</h1>
      <h2>Please upload an image</h2>
      <div className="card">
        <ImageUploader />
      </div>

    </div>
  )
}

export default App
