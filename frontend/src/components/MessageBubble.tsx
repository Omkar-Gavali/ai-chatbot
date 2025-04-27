'use client';
import { motion } from 'framer-motion'
import React from 'react';
import Image from 'next/image';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';


type Props = {
  text: string;
  isUser?: boolean;
};

const MessageBubble: React.FC<Props> = ({ text, isUser = false }) => {
  const backendUrl = 'http://localhost:8000';  // 👈 Your backend server

  return (
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

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className={`px-5 py-3 rounded-xl shadow-lg w-fit max-w-[75%] text-justify ${
          isUser ? 'bg-mint text-charcoal' : 'bg-lemon text-charcoal'
        }`}
       >
        {/* Render Markdown - with link fixing */}
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            a: ({ href = '', children }) => {
              const isInternalDataLink = href.startsWith('/data/');
              const fixedHref = isInternalDataLink ? `${backendUrl}${href}` : href;

              return (
                <a
                  href={fixedHref}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="underline text-blue-700"
                >
                  {children}
                </a>
              );
            },
          }}
        >
          {text}
        </ReactMarkdown>
      </motion.div>
    

      {isUser && (
        <Image
          src="/avatars/user.svg"
          width={32}
          height={32}
          alt="User"
          className="ml-2 rounded-full border border-white shadow-[0_2px_8px_rgba(0,0,0,0.15)]"
        />
      )}
    </div>
  );
};

export default MessageBubble;
