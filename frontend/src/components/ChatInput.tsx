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
    <div className="flex mt-4">
      <input
        type="text"
        className="flex-grow border rounded-l px-3 py-2 focus:outline-none"
        placeholder="Type your message..."
        value={message}
        onChange={e => setMessage(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleSend()}
      />
      <button
        className="px-4 py-2 bg-blue-600 text-white rounded-r hover:bg-blue-700"
        onClick={handleSend}
      >
        Send
      </button>
    </div>
  )
}

export default ChatInput
