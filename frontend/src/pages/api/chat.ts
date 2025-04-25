// frontend/src/pages/api/chat.ts
import type { NextApiRequest, NextApiResponse } from 'next'
import axios from 'axios'

type ChatResponse = { reply: string }

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ChatResponse | { error: string }>
) {
  console.log('⏱ /api/chat start:', new Date().toISOString())              // :contentReference[oaicite:1]{index=1}
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST'])
    return res.status(405).end(`Method ${req.method} Not Allowed`)
  }

  try {
    console.log('Parsing request body…', new Date().toISOString())
    const { message } = req.body

    console.log('Calling Cloud Run backend…', new Date().toISOString())
    const start = Date.now()
    const response = await axios.post(
      `${process.env.NEXT_PUBLIC_API_URL}/chat`, 
      { message }, 
      { headers: { 'Content-Type': 'application/json' } }
    )                                                                    // :contentReference[oaicite:2]{index=2}
    console.log('Backend responded in', Date.now() - start, 'ms')        // ﬁ

    console.log('Sending response to client…', new Date().toISOString())
    return res.status(200).json({ reply: response.data.reply })
  } catch (err: unknown) {
    console.error('💥 /api/chat error:', err)                             // :contentReference[oaicite:3]{index=3}
    const errorMessage = err instanceof Error ? err.message : 'Unknown error'
    return res.status(500).json({ error: errorMessage })
  }
}
