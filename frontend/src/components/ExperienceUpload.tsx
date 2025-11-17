import React, { useState } from 'react'
import { importExperiences } from '../api/client'
import './ExperienceUpload.css'

interface ExperienceUploadProps {
  onUploadSuccess?: () => void
  defaultCompanyName?: string
}

const ExperienceUpload: React.FC<ExperienceUploadProps> = ({ onUploadSuccess, defaultCompanyName = 'BEC' }) => {
  const [file, setFile] = useState<File | null>(null)
  const [companyName, setCompanyName] = useState<string>(defaultCompanyName)
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0]
      
      // Validate file type
      if (!selectedFile.name.endsWith('.xlsx') && !selectedFile.name.endsWith('.xls')) {
        setMessage({ type: 'error', text: 'Por favor selecciona un archivo Excel (.xlsx o .xls)' })
        setFile(null)
        return
      }
      
      setFile(selectedFile)
      setMessage(null)
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setMessage({ type: 'error', text: 'Por favor selecciona un archivo' })
      return
    }

    if (!companyName.trim()) {
      setMessage({ type: 'error', text: 'Por favor ingresa el nombre de la empresa' })
      return
    }

    setUploading(true)
    setMessage(null)

    try {
      const result = await importExperiences(file, companyName.trim())
      
      if (result.errors && result.errors.length > 0) {
        const errorText = result.errors.length > 3 
          ? `${result.errors.slice(0, 3).join(', ')}... (${result.errors.length} errores totales)`
          : result.errors.join(', ')
        setMessage({
          type: 'error',
          text: `${result.message}. Errores: ${errorText}`
        })
      } else {
        setMessage({ type: 'success', text: result.message })
        setFile(null)
        // Reset file input
        const fileInput = document.getElementById('excel-file-input') as HTMLInputElement
        if (fileInput) {
          fileInput.value = ''
        }
        
        if (onUploadSuccess) {
          onUploadSuccess()
        }
      }
    } catch (error) {
      setMessage({
        type: 'error',
        text: error instanceof Error ? error.message : 'Error al subir el archivo'
      })
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="experience-upload">
      <h3>Cargar Experiencias de la Empresa</h3>
      <p className="upload-description">
        Sube un archivo Excel con las experiencias de tu empresa para que el sistema pueda 
        encontrar licitaciones que coincidan con tu experiencia.
      </p>
      
      <div className="upload-form">
        <div className="form-group">
          <label htmlFor="company-name-input">Nombre de la Empresa:</label>
          <input
            type="text"
            id="company-name-input"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="Ej: BEC"
            disabled={uploading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="excel-file-input">Archivo Excel:</label>
          <input
            type="file"
            id="excel-file-input"
            accept=".xlsx,.xls"
            onChange={handleFileChange}
            disabled={uploading}
          />
          {file && (
            <div className="file-info">
              <span className="file-name">📄 {file.name}</span>
              <span className="file-size">
                ({(file.size / 1024).toFixed(2)} KB)
              </span>
            </div>
          )}
        </div>

        <button
          type="button"
          onClick={handleUpload}
          disabled={!file || uploading || !companyName.trim()}
          className="upload-button"
        >
          {uploading ? 'Subiendo...' : 'Subir Experiencias'}
        </button>
      </div>

      {message && (
        <div className={`upload-message ${message.type}`}>
          {message.type === 'success' && '✅ '}
          {message.type === 'error' && '❌ '}
          {message.text}
        </div>
      )}

      <div className="upload-help">
        <h4>Formato del archivo Excel:</h4>
        <ul>
          <li><strong>EMPRESA</strong> - Nombre de la empresa</li>
          <li><strong>CONTRATO No.</strong> - Número de contrato</li>
          <li><strong>OBRA</strong> - Descripción del proyecto (requerido)</li>
          <li><strong>ENTIDAD CONTRATANTE</strong> - Entidad que contrató</li>
          <li><strong>FECHA FINALIZACIÓN</strong> - Fecha de finalización</li>
          <li><strong>VALOR ACTUAL</strong> - Monto del contrato</li>
          <li><strong>CATEGORÍA</strong> - Categoría del proyecto</li>
          <li><strong>ÁREA DE LA INGENIERÍA CIVIL</strong> - Área de ingeniería</li>
        </ul>
      </div>
    </div>
  )
}

export default ExperienceUpload

