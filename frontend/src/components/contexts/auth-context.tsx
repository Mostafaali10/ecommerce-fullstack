'use client'

/**
 * AR: حالة المستخدم في الواجهة (ليست نفس JWT في الباكند — هنا للعرض والتنقل).
 * EN: Client-side auth state (separate from backend JWT — used for UI/navigation).
 */

import React, { createContext, useCallback, useContext, useMemo, useState } from 'react'

export type AuthUser = {
  id?: string
  email?: string
  name: string
  isAdmin: boolean
}

type AuthContextValue = {
  user: AuthUser | null
  isAuthenticated: boolean
  login: (user: AuthUser) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null)

  const login = useCallback((next: AuthUser) => {
    setUser(next)
  }, [])

  const logout = useCallback(() => {
    setUser(null)
  }, [])

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      login,
      logout,
    }),
    [user, login, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return ctx
}
