import React, { useState } from 'react'

type Props = {
  onSend: (message: string) => void
}

const ChatInput: React.FC<Props> = ({ onSend }) => {
  const [message, setMessage] = useState('')

  const handleSend = () => {
    if (!message.trim()) return
    onSend(message.trim())
    setMessage('')
  }

  return (
    <div className="flex w-full">
      <input
        type="text"
        className="flex-grow w-full border border-gray-300 rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-mint transition"        value={message}
        onChange={e => setMessage(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleSend()}
      />
      <button
        className="px-6 py-2 bg-mint text-white font-semibold rounded-r-lg hover:bg-lemon transition-colors"
        onClick={handleSend}
      >
        Send
      </button>
    </div>
  )
}

export default ChatInput
