'use client'

import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { Loader2 } from 'lucide-react'

interface ResultsDashboardProps {
  analysisId: string
}

export function ResultsDashboard({ analysisId }: ResultsDashboardProps) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['analysis', analysisId],
    queryFn: () => api.analysis.getStatus(analysisId),
    refetchInterval: (data) => 
      data?.status === 'completed' ? false : 2000
  })

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 flex items-center justify-center">
        <Loader2 className="animate-spin mr-2" />
        <span>Loading analysis results...</span>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 rounded-lg p-4 text-red-700">
        Error loading results
      </div>
    )
  }

  if (data?.status !== 'completed') {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 flex items-center justify-center">
        <Loader2 className="animate-spin mr-2" />
        <span>Analysis in progress...</span>
      </div>
    )
  }

  const results = data.results

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-semibold mb-4">Analysis Results</h2>
        
        {/* Technology Stack */}
        <div className="mb-8">
          <h3 className="text-lg font-medium mb-3">Technology Stack</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {results.technology?.technologies?.map((tech: string) => (
              <div key={tech} className="bg-gray-100 rounded px-3 py-2 text-sm">
                {tech}
              </div>
            ))}
          </div>
        </div>

        {/* Competitive Positioning */}
        <div className="mb-8">
          <h3 className="text-lg font-medium mb-3">Market Position</h3>
          <div className="bg-blue-50 rounded-lg p-4">
            <p className="text-gray-700">{results.positioning?.summary}</p>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <h4 className="font-medium text-gray-600">Performance Score</h4>
            <p className="text-2xl font-bold text-blue-600">
              {results.metrics?.performance || 'N/A'}
            </p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <h4 className="font-medium text-gray-600">SEO Score</h4>
            <p className="text-2xl font-bold text-green-600">
              {results.metrics?.seo || 'N/A'}
            </p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <h4 className="font-medium text-gray-600">UX Score</h4>
            <p className="text-2xl font-bold text-purple-600">
              {results.metrics?.ux || 'N/A'}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
