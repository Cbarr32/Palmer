'use client'

import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { AnalysisForm } from '@/components/AnalysisForm'
import { ResultsDashboard } from '@/components/ResultsDashboard'
import { api } from '@/lib/api'

export default function Home() {
  const [analysisId, setAnalysisId] = useState<string | null>(null)

  const analysisMutation = useMutation({
    mutationFn: api.analysis.quickScan,
    onSuccess: (data) => {
      setAnalysisId(data.id)
    },
  })

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Palmer Intelligence Platform
          </h1>
          <p className="text-xl text-gray-600">
            AI-Powered Competitive Analysis & Market Intelligence
          </p>
        </header>

        <div className="max-w-4xl mx-auto">
          <AnalysisForm onSubmit={analysisMutation.mutate} />
          
          {analysisId && (
            <ResultsDashboard analysisId={analysisId} />
          )}
        </div>
      </div>
    </main>
  )
}
