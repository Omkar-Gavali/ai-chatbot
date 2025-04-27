'use client';
import dynamic from 'next/dynamic';
import { useState } from 'react';
import ChatInput from '@/components/ChatInput';
import MessageBubble from '@/components/MessageBubble';

// Disable SSR for Lottie entirely
const Lottie = dynamic(() => import('lottie-react'), { ssr: false });
import smoothie from '../../public/smoothie.json';

interface Message {
  text: string;
  isUser: boolean;
}

export default function Home() {
  console.log("🔥 App Router page running 🔥");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const scrollToBottom = () => {
    if (typeof window !== 'undefined') {
      setTimeout(() => {
        document.getElementById('messageContainer')?.scrollTo({ top: 1e6, behavior: 'smooth' });
      }, 50);
    }
  };

  const handleSend = async (text: string) => {
    setMessages((msgs) => [...msgs, { text, isUser: true }]);
    scrollToBottom(); // 📍 Scroll after user's message immediately
    setLoading(true);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });
      const { reply } = await res.json();
      setMessages((msgs) => [...msgs, { text: reply, isUser: false }]);
    } catch {
      setMessages((msgs) => [...msgs, { text: 'Oops! Something went wrong.', isUser: false }]);
    } finally {
      setLoading(false);
      scrollToBottom(); // 📍 Scroll after bot's reply too
    }
  };

  return (
    <main className="h-screen w-full flex items-center justify-center bg-gradient-to-b from-charcoal to-gray-800 p-6">
      <div className="flex flex-col w-full max-w-lg h-[80vh] bg-white rounded-2xl border-2 border-charcoal shadow-2xl overflow-hidden">
        {/* Header */}
        <header className="bg-gradient-to-r from-mint to-lemon text-white text-5xl font-extrabold py-4 text-center">
          NutriBot🥝
        </header>

        {/* Accent Bar */}
        <div className="h-1 bg-gradient-to-r from-mint to-lemon" />

        {/* Messages */}
        <div className="relative flex-1 pt-7 pb-6 px-6 bg-gray-100 overflow-hidden">

        {/* Scrollable Messages */}
          <div
            id="messageContainer"
            className="h-full space-y-4 overflow-y-auto pr-2"
           >
            {/* 1. Placeholder: show only when no messages & not loading */}
            {!loading && messages.length === 0 && (
              <p className="text-gray-500 text-center">
                Your conversation will appear here.
              </p>
            )}

            {/* 2. Chat bubbles */}
            {messages.map((msg, i) => (
              <MessageBubble key={i} text={msg.text} isUser={msg.isUser} />
            ))}
          </div>

          

          {/* Loading Overlay */}
          {loading && (
            <div className="absolute inset-0 flex flex-col items-center justify-center bg-gray-100 bg-opacity-75 z-10">
              <Lottie
                animationData={smoothie}
                loop
                style={{ height: 100, width: 100 }}
              />
              <p className="mt-2 text-gray-600 italic">
                Blending your data… 🍌🍓🥤
              </p>
            </div>
          )}
        
        </div>

        {/* Divider */}
        <div className="border-t border-gray-200" />

        {/* Input */}
        <div className="border-t border-gray-200 bg-white px-6 py-6 flex justify-center items-center">
          <div className="w-full max-w-md">
            <ChatInput onSend={handleSend} />
          </div>
        </div>
      </div>
    </main>
  );
}
