import React, { useState } from 'react'
import MessageBubble from '../components/MessageBubble'
import ChatInput from '../components/ChatInput'
import axios from 'axios'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'


type Message = { text: string; isUser: boolean }

const HomePage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([])

  const sendMessage = async (text: string) => {
    const userMsg: Message = { text, isUser: true }
    setMessages(prev => [...prev, userMsg])

    try {
      const res = await axios.post('/api/chat', { message: text })
      const botMsg: Message = { text: res.data.reply, isUser: false }
      setMessages(prev => [...prev, botMsg])
    } catch (err) {
      console.error(err)
      toast.error('Error communicating with the chatbot.')
    }
  }

  return (
    <div className="max-w-xl mx-auto p-4">
      <h1 className="text-3xl font-extrabold mb-4 text-88d286">NutriBot 🍏</h1>
      <div className="h-[60vh] overflow-auto border rounded p-4 bg-white">
        {messages.map((m, idx) => (
          <MessageBubble key={idx} text={m.text} isUser={m.isUser} />
        ))}
      </div>
      <ChatInput onSend={sendMessage} />
      <ToastContainer position="bottom-center" />
    </div>
  )
}

export default HomePage
