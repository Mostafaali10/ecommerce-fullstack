'use client'

/**
 * AR: سلة التسوق في الذاكرة (يمكن لاحقاً ربطها بـ API الطلبات في الباكند).
 * EN: In-memory shopping cart (you can later connect it to the backend orders API).
 */

import React, { createContext, useCallback, useContext, useMemo, useState } from 'react'

export type CartLine = {
  id: string
  name: string
  price: number
  image: string
  category: string
  quantity: number
}

type AddPayload = {
  id: string
  name: string
  price: number
  image: string
  category: string
  quantity?: number
}

type CartContextValue = {
  items: CartLine[]
  addToCart: (item: AddPayload) => void
  cartCount: number
  cartTotal: number
}

const CartContext = createContext<CartContextValue | null>(null)

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<CartLine[]>([])

  const addToCart = useCallback((item: AddPayload) => {
    const qty = item.quantity ?? 1
    setItems((prev) => {
      const idx = prev.findIndex((line) => line.id === item.id)
      if (idx >= 0) {
        const next = [...prev]
        next[idx] = { ...next[idx], quantity: next[idx].quantity + qty }
        return next
      }
      return [
        ...prev,
        {
          id: item.id,
          name: item.name,
          price: item.price,
          image: item.image,
          category: item.category,
          quantity: qty,
        },
      ]
    })
  }, [])

  const cartCount = useMemo(() => items.reduce((sum, line) => sum + line.quantity, 0), [items])
  const cartTotal = useMemo(() => items.reduce((sum, line) => sum + line.price * line.quantity, 0), [items])

  const value = useMemo(
    () => ({
      items,
      addToCart,
      cartCount,
      cartTotal,
    }),
    [items, addToCart, cartCount, cartTotal],
  )

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}

export function useCart(): CartContextValue {
  const ctx = useContext(CartContext)
  if (!ctx) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return ctx
}
