'use client'
import Lottie from 'lottie-react'
import smoothie from '../../public/smoothie.json'
import { useState } from 'react'
import ChatInput from '@/components/ChatInput'
import MessageBubble from '@/components/MessageBubble'

interface Message {
  text: string
  isUser: boolean
}

export default function Home() {
  console.log("🔥 App Router page running 🔥");
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const handleSend = async (text: string) => {
    setLoading(true)
    setMessages(msgs => [...msgs, { text, isUser: true }])
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      })
      setLoading(false)
      const { reply } = await res.json()
      setMessages(msgs => [...msgs, { text: reply, isUser: false }])
    } catch {
      setMessages(msgs => [...msgs, { text: 'Oops! Something went wrong.', isUser: false }])
    }
    // At end of handleSend, after setMessages:
    setTimeout(() => {
      document
        .getElementById('messageContainer')
        ?.scrollTo({ top: 1e6, behavior: 'smooth' });
    }, 50)

  }

  return (
    
    <main className="h-screen w-full flex items-center justify-center bg-gradient-to-b from-charcoal to-gray-800 p-6">      
      <div className="flex flex-col w-full max-w-lg h-[80vh] bg-white rounded-2xl border-2 border-charcoal shadow-2xl overflow-hidden">
        {/* Header */}
        <header className="bg-gradient-to-r from-mint to-lemon text-white text-5xl font-extrabold py-4 text-center">

          NutriBot🥝
        </header>

        {/* Header ↕ Accent Bar */}
        <div className="h-1 bg-gradient-to-r from-mint to-lemon" />


        {/* Messages */}
        <div id="messageContainer" 
         className="flex-1 pt-7 pb-6 px-6 space-y-4 overflow-y-auto bg-gray-100 h-80"
        >
         
          
        
          {/* Loading Indicator */}
          {loading && (
            <div className="flex flex-col items-center py-4">
              <Lottie animationData={smoothie} loop={true} style={{ height: 100, width: 100 }} />
              <p className="mt-2 text-gray-600 italic">
                Blending your data…🍌🍓🥤
              </p>
            </div>
          )}
          {/* Placeholder message */}
          {messages.length === 0 ? (
            <p className="text-gray-500 text-center">
              Your conversation will appear here.
            </p>
          ) : (
            messages.map((msg, i) => (
              <MessageBubble key={i} text={msg.text} isUser={msg.isUser} />
            ))
          )}
        </div>

        {/* Divider */}
        <div className="border-t border-gray-200" />

        {/* Input */}
        <div className="border-t border-gray-200 bg-white px-6 py-6 flex justify-center items-center">
          <div className="w-full max-w-md ">
            <ChatInput onSend={handleSend} />
         </div>
        </div>
      </div>
    </main>
  )
}
