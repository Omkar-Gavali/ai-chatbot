// frontend/src/pages/index.tsx
import React, { useState } from 'react';
import axios from 'axios';
import MessageBubble from '../components/MessageBubble';
import ChatInput from '../components/ChatInput';

type Message = { text: string; isUser: boolean };

export default function HomePage() {
  const [messages, setMessages] = useState<Message[]>([]);

  const sendMessage = async (text: string) => {
    setMessages(prev => [...prev, { text, isUser: true }]);
    try {
      const res = await axios.post('/api/chat', { message: text });
      setMessages(prev => [...prev, { text: res.data.reply, isUser: false }]);
    } catch {
      setMessages(prev => [...prev, { text: 'Error: could not reach server.', isUser: false }]);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Nutrition & Beauty Bot</h1>
      <div className="h-[60vh] overflow-auto border rounded p-4 bg-white">
        {messages.map((m, i) => (
          <MessageBubble key={i} text={m.text} isUser={m.isUser} />
        ))}
      </div>
      <ChatInput onSend={sendMessage} />
    </div>
  );
}
