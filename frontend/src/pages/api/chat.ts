// frontend/src/pages/api/chat.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

type ChatResponse = { reply: string };

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ChatResponse | { error: string }>
) {
  const baseURL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
  console.log('Chat proxy calling:', `${baseURL}/chat`);

  try {
    const { message } = req.body;
    const response = await axios.post<ChatResponse>(
      `${baseURL}/chat`,
      { message }
    ); // Throws if ECONNREFUSED or non-2xx :contentReference[oaicite:1]{index=1}
    
    // Forward the backend’s reply
    return res.status(200).json({ reply: response.data.reply });
  } catch (err: any) {
    console.error('Chat API error:', err);
    // Return error message to front end
    return res.status(500).json({ error: 'Failed to fetch from backend.' });
  }
}
