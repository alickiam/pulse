import { createContext, useContext, useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Cookies from 'js-cookie'

type User = {
  username: string
  firstName: string
  lastName: string
  improvement: string | null
}

type UserContextType = {
  user: User | null
  login: (user: User) => void
  logout: () => void
  isLoading: boolean
}

const UserContext = createContext<UserContextType | undefined>(undefined)

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  // Function to fetch latest user data from the database
  const fetchLatestUserData = async (username: string) => {
    try {
      const response = await fetch(`/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          username,
          // Send a special flag to indicate this is just a data refresh
          isRefresh: true 
        })
      })

      const data = await response.json()
      if (data.success && data.user) {
        setUser(data.user)
        Cookies.set('userData', JSON.stringify(data.user))
      }
    } catch (error) {
      console.error('Failed to refresh user data:', error)
    }
  }

  // Check cookies and fetch latest data on mount
  useEffect(() => {
    const userData = Cookies.get('userData')
    if (userData) {
      try {
        const parsedUser = JSON.parse(userData)
        setUser(parsedUser)
        // Immediately fetch latest data
        fetchLatestUserData(parsedUser.username)
      } catch (e) {
        Cookies.remove('userData')
      }
    }
    setIsLoading(false)
  }, [])

  // Fetch latest data periodically while user is logged in
  useEffect(() => {
    if (!user?.username) return

    const interval = setInterval(() => {
      fetchLatestUserData(user.username)
    }, 30000) // Refresh every 30 seconds

    return () => clearInterval(interval)
  }, [user?.username])

  const login = (userData: User) => {
    setUser(userData)
    Cookies.set('userData', JSON.stringify(userData))
  }

  const logout = () => {
    setUser(null)
    Cookies.remove('userData')
    router.push('/login')
  }

  return (
    <UserContext.Provider value={{ user, login, logout, isLoading }}>
      {children}
    </UserContext.Provider>
  )
}

export function useUser() {
  const context = useContext(UserContext)
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider')
  }
  return context
} 