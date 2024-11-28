import { useUser } from '@/lib/hooks/useUser'
import { useRouter } from 'next/router'
import { useEffect } from 'react'

export function withAuth<P extends object>(
  WrappedComponent: React.ComponentType<P>
) {
  return function ProtectedRoute(props: P) {
    const { user, isLoading } = useUser()
    const router = useRouter()

    useEffect(() => {
      if (!isLoading && !user) {
        router.replace('/login')
      }
    }, [user, isLoading, router])

    if (isLoading) {
      return (
        <div className="min-h-screen bg-gray-900 flex justify-center items-center">
          <div className="text-2xl font-bold bg-gradient-to-r from-purple-400 via-pink-300 to-red-400 text-transparent bg-clip-text animate-pulse">
            Loading...
          </div>
        </div>
      )
    }

    if (!user) {
      return null
    }

    return <WrappedComponent {...props} />
  }
} 