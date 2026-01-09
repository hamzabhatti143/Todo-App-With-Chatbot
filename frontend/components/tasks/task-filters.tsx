/**
 * Task Filters Component
 *
 * Filter controls with Tabs for status filtering, sort dropdown,
 * task count badges, and clear filters button.
 */

'use client';

import { motion } from 'framer-motion';
import { ArrowUpDown, RotateCcw } from 'lucide-react';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Dropdown,
  DropdownTrigger,
  DropdownContent,
  DropdownItem,
  DropdownLabel,
  DropdownSeparator,
} from '@/components/ui/dropdown';
import { Button } from '@/components/ui/button';
import type { FilterType, SortType } from '@/types/task';

interface TaskFiltersProps {
  filter: FilterType;
  onFilterChange: (filter: FilterType) => void;
  sort: SortType;
  onSortChange: (sort: SortType) => void;
  taskCounts: {
    all: number;
    active: number;
    completed: number;
  };
  onClearFilters: () => void;
  className?: string;
}

const sortOptions: { value: SortType; label: string }[] = [
  { value: 'newest', label: 'Newest first' },
  { value: 'oldest', label: 'Oldest first' },
  { value: 'title-asc', label: 'Title (A-Z)' },
  { value: 'title-desc', label: 'Title (Z-A)' },
];

export function TaskFilters({
  filter,
  onFilterChange,
  sort,
  onSortChange,
  taskCounts,
  onClearFilters,
  className,
}: TaskFiltersProps) {
  const getSortLabel = () => {
    return sortOptions.find((opt) => opt.value === sort)?.label || 'Sort by';
  };

  return (
    <div className={className}>
      <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        {/* Filter Tabs */}
        <Tabs value={filter} onValueChange={(value) => onFilterChange(value as FilterType)}>
          <TabsList>
            <TabsTrigger value="all">
              All
              <TaskCountBadge count={taskCounts.all} active={filter === 'all'} />
            </TabsTrigger>
            <TabsTrigger value="active">
              Active
              <TaskCountBadge count={taskCounts.active} active={filter === 'active'} />
            </TabsTrigger>
            <TabsTrigger value="completed">
              Completed
              <TaskCountBadge count={taskCounts.completed} active={filter === 'completed'} />
            </TabsTrigger>
          </TabsList>
        </Tabs>

        {/* Actions */}
        <div className="flex items-center gap-2">
          {/* Sort Dropdown */}
          <Dropdown>
            <DropdownTrigger asChild>
              <Button variant="secondary" size="sm">
                <ArrowUpDown className="h-4 w-4 mr-2" />
                {getSortLabel()}
              </Button>
            </DropdownTrigger>

            <DropdownContent align="end">
              <DropdownLabel>Sort by</DropdownLabel>
              <DropdownSeparator />
              {sortOptions.map((option) => (
                <DropdownItem
                  key={option.value}
                  onClick={() => onSortChange(option.value)}
                  className={sort === option.value ? 'bg-gray-100 dark:bg-gray-700' : ''}
                >
                  {option.label}
                  {sort === option.value && (
                    <span className="ml-auto text-blue-600 dark:text-blue-400">✓</span>
                  )}
                </DropdownItem>
              ))}
            </DropdownContent>
          </Dropdown>

          {/* Clear Filters Button */}
          {(filter !== 'all' || sort !== 'newest') && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ duration: 0.2 }}
            >
              <Button
                variant="ghost"
                size="sm"
                onClick={onClearFilters}
                className="text-gray-600 dark:text-gray-400"
              >
                <motion.div
                  whileHover={{ rotate: 180 }}
                  transition={{ duration: 0.3 }}
                >
                  <RotateCcw className="h-4 w-4 mr-2" />
                </motion.div>
                Clear
              </Button>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}

/**
 * Task Count Badge Component
 */
interface TaskCountBadgeProps {
  count: number;
  active: boolean;
}

function TaskCountBadge({ count, active }: TaskCountBadgeProps) {
  return (
    <motion.span
      className={`ml-2 px-2 py-0.5 rounded-full text-xs font-medium ${
        active
          ? 'bg-blue-500 text-white'
          : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
      }`}
      layout
      transition={{ duration: 0.2 }}
    >
      {count}
    </motion.span>
  );
}
