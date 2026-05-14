/**
 * AR: أنواع بسيطة لـ `use-toast` (متوافقة مع shadcn).
 * EN: Minimal toast types for `use-toast` (shadcn-compatible).
 */

import * as React from 'react'

export type ToastProps = {
  open?: boolean
  onOpenChange?: (open: boolean) => void
}

export type ToastActionElement = React.ReactElement<{ altText?: string }>
