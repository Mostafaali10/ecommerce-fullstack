'use client'

import { useEffect, useState } from 'react'
import { Card } from '@/components/ui/card'
import { productService, orderService, categoryService } from '@/lib/api'
import { Package, ShoppingCart, DollarSign, Users } from 'lucide-react'

function StatCard({
  title,
  value,
  icon: Icon,
  color,
}: {
  title: string
  value: string | number
  icon: any
  color: string
}) {
  return (
    <Card className="p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-muted-foreground">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${color}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </Card>
  )
}

export default function AdminDashboard() {
  const [products, setProducts] = useState<any[]>([])
  const [orders, setOrders] = useState<any[]>([])
  const [categories, setCategories] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchData() {
      try {
        const [prods, ords, cats] = await Promise.all([
          productService.getProducts().catch(() => []),
          orderService.getMyOrders().catch(() => []),
          categoryService.getCategories().catch(() => []),
        ])
        setProducts(prods)
        setOrders(ords)
        setCategories(cats)
      } catch (e) {
        // الباك إند مش شغال — نعرض أصفار
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const recentOrders = [...orders].reverse().slice(0, 5)

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-screen">
        <p className="text-muted-foreground text-lg">Loading dashboard...</p>
      </div>
    )
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Products"
          value={products.length}
          icon={Package}
          color="bg-blue-500"
        />
        <StatCard
          title="Total Orders"
          value={orders.length}
          icon={ShoppingCart}
          color="bg-green-500"
        />
        <StatCard
          title="Total Categories"
          value={categories.length}
          icon={DollarSign}
          color="bg-purple-500"
        />
        <StatCard
          title="Recent Orders"
          value={recentOrders.length}
          icon={Users}
          color="bg-orange-500"
        />
      </div>

      {/* Recent Orders */}
      <Card className="p-6">
        <h2 className="text-lg font-bold mb-4">Recent Orders</h2>
        {recentOrders.length === 0 ? (
          <p className="text-muted-foreground">No orders yet — make sure the backend is running on port 8000.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 px-4">Order ID</th>
                  <th className="text-left py-3 px-4">Date</th>
                  <th className="text-left py-3 px-4">Items</th>
                  <th className="text-left py-3 px-4">Status</th>
                </tr>
              </thead>
              <tbody>
                {recentOrders.map((order: any) => (
                  <tr key={order.id} className="border-b border-border">
                    <td className="py-3 px-4 font-mono text-xs">#{order.id}</td>
                    <td className="py-3 px-4">
                      {new Date(order.created_at).toLocaleDateString()}
                    </td>
                    <td className="py-3 px-4">{order.items?.length ?? 0}</td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-1 rounded text-xs font-medium bg-blue-100 text-blue-800">
                        {order.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  )
}
