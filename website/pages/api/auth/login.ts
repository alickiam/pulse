import { PrismaClient } from '@prisma/client'
import type { NextApiRequest, NextApiResponse } from 'next'

const prisma = new PrismaClient()

type LoginResponse = {
  success: boolean
  message: string
  user?: {
    username: string
    firstName: string
    lastName: string
    improvement: string | null
  }
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<LoginResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' })
  }

  try {
    const { username, password, isRefresh } = req.body

    if (!username) {
      return res.status(400).json({
        success: false,
        message: 'Username is required'
      })
    }

    const user = await prisma.user.findUnique({
      where: { username }
    })

    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'Invalid username or password'
      })
    }

    // Skip password check if this is just a refresh request
    if (!isRefresh && password !== user.password) {
      return res.status(401).json({
        success: false,
        message: 'Invalid username or password'
      })
    }

    return res.status(200).json({
      success: true,
      message: isRefresh ? 'User data refreshed' : 'Login successful',
      user: {
        username: user.username,
        firstName: user.first_name,
        lastName: user.last_name,
        improvement: user.improvement
      }
    })
  } catch (error) {
    console.error('Login error:', error)
    return res.status(500).json({
      success: false,
      message: 'Internal server error'
    })
  } finally {
    await prisma.$disconnect()
  }
} 