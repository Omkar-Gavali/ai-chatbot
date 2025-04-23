// frontend/src/components/ChatInput.tsx
import React, { useState } from 'react';

type Props = {
  onSend: (message: string) => void;
};

export default function ChatInput({ onSend }: Props) {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (!message.trim()) return;
    onSend(message.trim());
    setMessage('');
  };

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
        onClick={handleSend}
        className="bg-blue-600 text-white px-4 py-2 rounded-r hover:bg-blue-700"
      >
        Send
      </button>
    </div>
  );
}
