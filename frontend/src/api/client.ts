import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Tender {
  id: string
  external_id: string
  source: string
  entity_name: string
  object_text: string
  department: string | null
  municipality: string | null
  amount: number | null
  publication_date: string | null
  closing_date: string | null
  state: string
  process_url: string
  contract_type: string | null
  contract_modality: string | null
  relevance_score: number | null
  is_relevant_interventoria_vial: boolean
  created_at: string
  updated_at: string
}

export interface TenderListResponse {
  items: Tender[]
  total: number
  limit: number
  offset: number
}

export interface TenderFilters {
  is_relevant?: boolean
  department?: string
  contract_type?: string
  contract_modality?: string
  date_from?: string
  date_to?: string
  limit?: number
  offset?: number
}

export async function getTenders(filters: TenderFilters = {}): Promise<TenderListResponse> {
  const params = new URLSearchParams()
  
  if (filters.is_relevant !== undefined) {
    params.append('is_relevant', filters.is_relevant.toString())
  }
  if (filters.department) {
    params.append('department', filters.department)
  }
  if (filters.contract_type) {
    params.append('contract_type', filters.contract_type)
  }
  if (filters.contract_modality) {
    params.append('contract_modality', filters.contract_modality)
  }
  if (filters.date_from) {
    params.append('date_from', filters.date_from)
  }
  if (filters.date_to) {
    params.append('date_to', filters.date_to)
  }
  if (filters.limit) {
    params.append('limit', filters.limit.toString())
  }
  if (filters.offset) {
    params.append('offset', filters.offset.toString())
  }
  
  const response = await client.get<TenderListResponse>(`/tenders?${params.toString()}`)
  return response.data
}

export async function getTender(id: string): Promise<Tender> {
  const response = await client.get<Tender>(`/tenders/${id}`)
  return response.data
}

