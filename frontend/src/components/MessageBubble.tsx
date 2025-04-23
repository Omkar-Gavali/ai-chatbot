import React from 'react'

type Props = {
  text: string
  isUser?: boolean
}

const MessageBubble: React.FC<Props> = ({ text, isUser = false }) => (
  <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-2`}>
    <div
      className={`max-w-xs px-4 py-2 rounded-lg ${
        isUser ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'
      }`}
    >
      {text}
    </div>
  </div>
)

export default MessageBubble
