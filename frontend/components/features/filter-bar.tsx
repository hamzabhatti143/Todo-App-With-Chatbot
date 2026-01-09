/**
 * Filter Bar Component
 *
 * Provides filter buttons for task completion status.
 */

'use client'

import { Button } from '@/components/ui/button'
import type { FilterType } from '@/types/task'

interface FilterBarProps {
  activeFilter: FilterType
  onFilterChange: (filter: FilterType) => void
  taskCounts?: {
    all: number
    active: number
    completed: number
  }
}

export function FilterBar({ activeFilter, onFilterChange, taskCounts }: FilterBarProps) {
  const filters: { key: FilterType; label: string }[] = [
    { key: 'all', label: 'All Tasks' },
    { key: 'active', label: 'Active' },
    { key: 'completed', label: 'Completed' },
  ]

  return (
    <div className="flex flex-wrap gap-2 mb-6">
      {filters.map((filter) => {
        const isActive = activeFilter === filter.key
        const count = taskCounts?.[filter.key]

        return (
          <Button
            key={filter.key}
            variant={isActive ? 'primary' : 'secondary'}
            size="sm"
            onClick={() => onFilterChange(filter.key)}
            className={`transition-all ${
              isActive ? 'ring-2 ring-blue-300' : ''
            }`}
          >
            {filter.label}
            {count !== undefined && (
              <span className={`ml-2 px-2 py-0.5 rounded-full text-xs ${
                isActive ? 'bg-blue-500 text-white' : 'bg-gray-300 text-gray-700'
              }`}>
                {count}
              </span>
            )}
          </Button>
        )
      })}
    </div>
  )
}
