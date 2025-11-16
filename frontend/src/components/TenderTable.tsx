import React from 'react'
import { Tender } from '../api/client'
import './TenderTable.css'

interface TenderTableProps {
  tenders: Tender[]
}

const TenderTable: React.FC<TenderTableProps> = ({ tenders }) => {
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
  
  const formatRelevanceScore = (score: number | null): string => {
    if (score === null) return 'N/A'
    return (score * 100).toFixed(0) + '%'
  }
  
  if (tenders.length === 0) {
    return (
      <div className="tender-table-empty">
        <p>No se encontraron licitaciones con los filtros seleccionados.</p>
      </div>
    )
  }
  
  return (
    <div className="tender-table-container">
      <table className="tender-table">
        <thead>
          <tr>
            <th>Fecha Publicación</th>
            <th>Entidad</th>
            <th>Departamento</th>
            <th>Tipo de Contrato</th>
            <th>Monto</th>
            <th>Relevancia</th>
            <th>Enlace</th>
          </tr>
        </thead>
        <tbody>
          {tenders.map((tender) => (
            <tr key={tender.id}>
              <td>{formatDate(tender.publication_date)}</td>
              <td className="entity-cell">
                <div className="entity-name">{tender.entity_name}</div>
                <div className="object-preview">
                  {tender.object_text.substring(0, 100)}
                  {tender.object_text.length > 100 ? '...' : ''}
                </div>
              </td>
              <td>{tender.department || 'N/A'}</td>
              <td>{tender.contract_type || 'N/A'}</td>
              <td className="amount-cell">{formatCurrency(tender.amount)}</td>
              <td>
                <span className={`relevance-badge ${tender.is_relevant_interventoria_vial ? 'relevant' : 'not-relevant'}`}>
                  {formatRelevanceScore(tender.relevance_score)}
                </span>
              </td>
              <td>
                <a
                  href={tender.process_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="process-link"
                >
                  Ver proceso
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default TenderTable

