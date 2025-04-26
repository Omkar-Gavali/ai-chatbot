// src/components/MessageBubble.tsx

import React from 'react';
import Image from 'next/image';

type Props = {
  text: string;
  isUser?: boolean;
};

const MessageBubble: React.FC<Props> = ({ text, isUser = false }) => (
  <div className={`flex items-start mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
    {!isUser && (
      <Image
        src="/avatars/nutribot.svg"
        width={32}
        height={32}
        alt="NutriBot"
        className="mr-2 rounded-full border-2 border-white shadow-md"
      />
    )}
    <div
      className={`max-w-xs px-5 py-3 rounded-xl shadow-lg ${
        isUser ?  'bg-mint text-charcoal' : 'bg-lemon text-charcoal'
      }`}
    >
      {text}
    </div>
    {isUser && (
      <Image
        src="/avatars/user.svg"
        width={32}
        height={32}
        alt="User"
        className="mr-2 rounded-full border border-white shadow-[0_2px_8px_rgba(0,0,0,0.15)]"
      />
    )}
  </div>
);

export default MessageBubble;



