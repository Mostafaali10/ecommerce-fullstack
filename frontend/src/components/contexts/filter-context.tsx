'use client'

/**
 * AR: فلاتر صفحة المنتجات (بحث، تصنيف، نطاق سعر).
 * EN: Product listing filters (search, category, price range).
 */

import React, { createContext, useCallback, useContext, useMemo, useState } from 'react'

type FilterContextValue = {
  searchQuery: string
  setSearchQuery: (value: string) => void
  selectedCategory: string
  setSelectedCategory: (value: string) => void
  priceRange: [number, number]
  setPriceRange: (value: [number, number]) => void
  resetFilters: () => void
}

const FilterContext = createContext<FilterContextValue | null>(null)

export function FilterProvider({ children }: { children: React.ReactNode }) {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [priceRange, setPriceRange] = useState<[number, number]>([0, 1000])

  const resetFilters = useCallback(() => {
    setSearchQuery('')
    setSelectedCategory('all')
    setPriceRange([0, 1000])
  }, [])

  const value = useMemo(
    () => ({
      searchQuery,
      setSearchQuery,
      selectedCategory,
      setSelectedCategory,
      priceRange,
      setPriceRange,
      resetFilters,
    }),
    [searchQuery, selectedCategory, priceRange, resetFilters],
  )

  return <FilterContext.Provider value={value}>{children}</FilterContext.Provider>
}

export function useFilters(): FilterContextValue {
  const ctx = useContext(FilterContext)
  if (!ctx) {
    throw new Error('useFilters must be used within a FilterProvider')
  }
  return ctx
}
