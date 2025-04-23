// frontend/src/components/MessageBubble.tsx
import React from 'react';

type Props = {
  text: string;
  isUser?: boolean;
};

export default function MessageBubble({ text, isUser = false }: Props) {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-2`}>
      <div className={`${isUser ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'} rounded-lg px-4 py-2 max-w-xs`}>
        {text}
      </div>
    </div>
  );
}
