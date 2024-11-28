import { PrismaClient } from '@prisma/client'
import type { NextApiRequest, NextApiResponse } from 'next'

const prisma = new PrismaClient()

type PairResponse = {
  success: boolean
  message: string
  pairs?: {
    pairid: number
    partner: {
      username: string
      firstName: string
      lastName: string
    }
    result?: {
      affection: number
      vulnerability: number
      kindness: number
      other: number
      negative: number
      explanation: string
      rate: number
      convo: number
      total: number
      match_status: number
    } | null
  }[]
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<PairResponse>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ success: false, message: 'Method not allowed' })
  }

  try {
    const { username } = req.query

    if (!username || typeof username !== 'string') {
      return res.status(400).json({
        success: false,
        message: 'Username is required'
      })
    }

    // Get all pairs where the user is either id1 or id2
    const pairs = await prisma.pair.findMany({
      where: {
        OR: [
          { id1: username },
          { id2: username }
        ]
      },
      include: {
        user1: {
          select: {
            username: true,
            first_name: true,
            last_name: true
          }
        },
        user2: {
          select: {
            username: true,
            first_name: true,
            last_name: true
          }
        },
        result: true
      }
    })

    // Transform the data to return the partner's info instead of both users
    const formattedPairs = pairs.map(pair => ({
      pairid: pair.pairid,
      partner: {
        username: pair.id1 === username ? pair.user2.username : pair.user1.username,
        firstName: pair.id1 === username ? pair.user2.first_name : pair.user1.first_name,
        lastName: pair.id1 === username ? pair.user2.last_name : pair.user1.last_name
      },
      result: pair.result
    }))

    return res.status(200).json({
      success: true,
      message: 'Pairs retrieved successfully',
      pairs: formattedPairs
    })
  } catch (error) {
    console.error('Get pairs error:', error)
    return res.status(500).json({
      success: false,
      message: 'Internal server error'
    })
  } finally {
    await prisma.$disconnect()
  }
}