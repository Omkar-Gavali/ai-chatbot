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
        className="mr-2"
      />
    )}
    <div
      className={`max-w-xs px-4 py-2 rounded-lg ${
        isUser ? 'bg-mint text-darkbg' : 'bg-lemon text-darkbg'
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
        className="ml-2"
      />
    )}
  </div>
);

export default MessageBubble;



