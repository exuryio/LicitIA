import React from 'react'
import { CompanyExperience } from '../api/client'
import { deleteExperience } from '../api/client'
import './ExperienceList.css'

interface ExperienceListProps {
  experiences: CompanyExperience[]
  companyName: string
  onDelete?: () => void
}

const ExperienceList: React.FC<ExperienceListProps> = ({ experiences, companyName, onDelete }) => {
  const formatDate = (dateString: string | null): string => {
    if (!dateString) return 'N/A'
    try {
      return new Date(dateString).toLocaleDateString('es-CO')
    } catch {
      return 'N/A'
    }
  }

  const formatCurrency = (amount: number | null): string => {
    if (!amount) return 'N/A'
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount)
  }

  const handleDelete = async (id: string) => {
    if (!window.confirm('¿Estás seguro de que deseas eliminar esta experiencia?')) {
      return
    }

    try {
      await deleteExperience(id)
      if (onDelete) {
        onDelete()
      }
    } catch (error) {
      alert('Error al eliminar la experiencia: ' + (error instanceof Error ? error.message : 'Error desconocido'))
    }
  }

  if (experiences.length === 0) {
    return (
      <div className="experience-list-empty">
        <p>No se encontraron experiencias para "{companyName}".</p>
        <p>Sube un archivo Excel para comenzar.</p>
      </div>
    )
  }

  return (
    <div className="experience-list">
      <div className="experience-list-header">
        <p className="experience-count">
          {experiences.length} {experiences.length === 1 ? 'experiencia encontrada' : 'experiencias encontradas'}
        </p>
      </div>

      <div className="experience-grid">
        {experiences.map((experience) => (
          <div key={experience.id} className="experience-card">
            <div className="experience-card-header">
              <h3 className="experience-project">
                {experience.project_description.length > 80
                  ? experience.project_description.substring(0, 80) + '...'
                  : experience.project_description}
              </h3>
              <button
                className="delete-button"
                onClick={() => handleDelete(experience.id)}
                title="Eliminar experiencia"
              >
                ×
              </button>
            </div>

            <div className="experience-card-body">
              {experience.contracting_entity && (
                <div className="experience-field">
                  <span className="field-label">Entidad:</span>
                  <span className="field-value">{experience.contracting_entity}</span>
                </div>
              )}

              {experience.contract_number && (
                <div className="experience-field">
                  <span className="field-label">Contrato:</span>
                  <span className="field-value">{experience.contract_number}</span>
                </div>
              )}

              {experience.completion_date && (
                <div className="experience-field">
                  <span className="field-label">Fecha Finalización:</span>
                  <span className="field-value">{formatDate(experience.completion_date)}</span>
                </div>
              )}

              {experience.amount && (
                <div className="experience-field">
                  <span className="field-label">Valor:</span>
                  <span className="field-value amount">{formatCurrency(experience.amount)}</span>
                </div>
              )}

              {experience.category && (
                <div className="experience-field">
                  <span className="field-label">Categoría:</span>
                  <span className="field-value">{experience.category}</span>
                </div>
              )}

              {experience.engineering_area && (
                <div className="experience-field">
                  <span className="field-label">Área:</span>
                  <span className="field-value">{experience.engineering_area}</span>
                </div>
              )}

              {experience.keywords && experience.keywords.length > 0 && (
                <div className="experience-field">
                  <span className="field-label">Palabras clave:</span>
                  <div className="keywords-list">
                    {experience.keywords.slice(0, 5).map((keyword, idx) => (
                      <span key={idx} className="keyword-tag">
                        {keyword}
                      </span>
                    ))}
                    {experience.keywords.length > 5 && (
                      <span className="keyword-more">+{experience.keywords.length - 5} más</span>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ExperienceList

