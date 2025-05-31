'use client'

import { useState } from 'react'
import { Search } from 'lucide-react'

interface AnalysisFormProps {
  onSubmit: (data: any) => void
}

export function AnalysisForm({ onSubmit }: AnalysisFormProps) {
  const [targetUrl, setTargetUrl] = useState('')
  const [competitors, setCompetitors] = useState<string[]>([''])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit({
      target_url: targetUrl,
      competitors: competitors.filter(c => c.length > 0)
    })
  }

  const addCompetitor = () => {
    setCompetitors([...competitors, ''])
  }

  const updateCompetitor = (index: number, value: string) => {
    const updated = [...competitors]
    updated[index] = value
    setCompetitors(updated)
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 className="text-2xl font-semibold mb-6">Start Analysis</h2>
      
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Target Website
        </label>
        <input
          type="url"
          value={targetUrl}
          onChange={(e) => setTargetUrl(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          placeholder="https://example.com"
          required
        />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Competitors (Optional)
        </label>
        {competitors.map((comp, index) => (
          <input
            key={index}
            type="url"
            value={comp}
            onChange={(e) => updateCompetitor(index, e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md mb-2"
            placeholder="https://competitor.com"
          />
        ))}
        <button
          type="button"
          onClick={addCompetitor}
          className="text-blue-600 hover:text-blue-800 text-sm"
        >
          + Add another competitor
        </button>
      </div>

      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 flex items-center justify-center gap-2"
      >
        <Search size={20} />
        Analyze
      </button>
    </form>
  )
}
