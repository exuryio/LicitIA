import React, { useState, useEffect } from 'react'
import FiltersBar from '../components/FiltersBar'
import TenderTable from '../components/TenderTable'
import { getTenders, Tender, TenderFilters } from '../api/client'
import './Dashboard.css'

const Dashboard: React.FC = () => {
  const [tenders, setTenders] = useState<Tender[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [total, setTotal] = useState(0)
  
  // Filter state
  const [filters, setFilters] = useState<TenderFilters>({
    is_relevant: true,
    limit: 50,
    offset: 0,
  })
  
  const [dateFrom, setDateFrom] = useState<string>('')
  const [dateTo, setDateTo] = useState<string>('')
  const [department, setDepartment] = useState<string>('')
  const [contractType, setContractType] = useState<string>('')
  const [onlyRelevant, setOnlyRelevant] = useState<boolean>(true)
  
  const fetchTenders = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const params: TenderFilters = {
        is_relevant: onlyRelevant,
        limit: 50,
        offset: 0,
      }
      
      if (dateFrom) {
        params.date_from = dateFrom
      }
      if (dateTo) {
        params.date_to = dateTo
      }
      if (department) {
        params.department = department
      }
      if (contractType) {
        params.contract_type = contractType
      }
      
      const response = await getTenders(params)
      setTenders(response.items)
      setTotal(response.total)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al cargar licitaciones')
      console.error('Error fetching tenders:', err)
    } finally {
      setLoading(false)
    }
  }
  
  useEffect(() => {
    fetchTenders()
  }, [])
  
  const handleFilterSubmit = () => {
    fetchTenders()
  }
  
  return (
    <div className="dashboard">
      <FiltersBar
        dateFrom={dateFrom}
        dateTo={dateTo}
        department={department}
        contractType={contractType}
        onlyRelevant={onlyRelevant}
        onDateFromChange={setDateFrom}
        onDateToChange={setDateTo}
        onDepartmentChange={setDepartment}
        onContractTypeChange={setContractType}
        onOnlyRelevantChange={setOnlyRelevant}
        onSubmit={handleFilterSubmit}
      />
      
      {loading && <div className="loading">Cargando...</div>}
      {error && <div className="error">Error: {error}</div>}
      
      {!loading && !error && (
        <div className="results-info">
          <p>Mostrando {tenders.length} de {total} licitaciones</p>
        </div>
      )}
      
      {!loading && !error && (
        <TenderTable tenders={tenders} />
      )}
    </div>
  )
}

export default Dashboard

