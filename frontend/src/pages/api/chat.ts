// frontend/src/pages/api/chat.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

type ChatResponse = { reply: string };

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ChatResponse | { error: string }>
) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }

  try {
    const { message } = req.body as { message: string };
    // ... axios call and forwarding logic ...
  } catch (err: unknown) {
    console.error('Chat API error:', err);
    // Narrow to Error to safely access .message if needed
    const errorMessage =
      err instanceof Error ? err.message : 'Unknown error';
    return res.status(500).json({ error: errorMessage });
  }
}
