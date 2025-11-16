import React from 'react'
import './FiltersBar.css'
import { CONTRACT_TYPES } from '../constants/contractTypes'

interface FiltersBarProps {
  dateFrom: string
  dateTo: string
  department: string
  contractType: string
  onlyRelevant: boolean
  onDateFromChange: (value: string) => void
  onDateToChange: (value: string) => void
  onDepartmentChange: (value: string) => void
  onContractTypeChange: (value: string) => void
  onOnlyRelevantChange: (value: boolean) => void
  onSubmit: () => void
}

const FiltersBar: React.FC<FiltersBarProps> = ({
  dateFrom,
  dateTo,
  department,
  contractType,
  onlyRelevant,
  onDateFromChange,
  onDateToChange,
  onDepartmentChange,
  onContractTypeChange,
  onOnlyRelevantChange,
  onSubmit,
}) => {
  return (
    <div className="filters-bar">
      <h2>Filtros</h2>
      <form
        onSubmit={(e) => {
          e.preventDefault()
          onSubmit()
        }}
      >
        <div className="filters-grid">
          <div className="filter-group">
            <label htmlFor="dateFrom">Fecha desde:</label>
            <input
              type="date"
              id="dateFrom"
              value={dateFrom}
              onChange={(e) => onDateFromChange(e.target.value)}
            />
          </div>
          
          <div className="filter-group">
            <label htmlFor="dateTo">Fecha hasta:</label>
            <input
              type="date"
              id="dateTo"
              value={dateTo}
              onChange={(e) => onDateToChange(e.target.value)}
            />
          </div>
          
          <div className="filter-group">
            <label htmlFor="department">Departamento:</label>
            <input
              type="text"
              id="department"
              placeholder="Ej: Cundinamarca"
              value={department}
              onChange={(e) => onDepartmentChange(e.target.value)}
            />
          </div>
          
          <div className="filter-group">
            <label htmlFor="contractType">Tipo de contrato:</label>
            <select
              id="contractType"
              value={contractType}
              onChange={(e) => onContractTypeChange(e.target.value)}
            >
              {CONTRACT_TYPES.map((type) => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>
          
          <div className="filter-group checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={onlyRelevant}
                onChange={(e) => onOnlyRelevantChange(e.target.checked)}
              />
              Solo interventoría vial relevante
            </label>
          </div>
        </div>
        
        <button type="submit" className="submit-button">
          Buscar
        </button>
      </form>
    </div>
  )
}

export default FiltersBar

