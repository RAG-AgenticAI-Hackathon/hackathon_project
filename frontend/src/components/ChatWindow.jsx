import { useRef, useEffect } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Message } from './Message';
import { LoadingDots } from './LoadingDots';
import { WelcomeScreen } from './WelcomeScreen';

export function ChatWindow({ messages, isLoading, onSelectQuestion }) {
  const bottomRef = useRef(null);

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const isEmpty = messages.length === 0;

  return (
    <div className="flex-1 overflow-hidden relative">
      <AnimatePresence mode="wait">
        {isEmpty ? (
          <motion.div
            key="welcome"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="h-full"
          >
            <WelcomeScreen onSelectQuestion={onSelectQuestion} />
          </motion.div>
        ) : (
          <motion.div
            key="chat"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.2 }}
            className="h-full overflow-y-auto px-3 sm:px-4 py-4 sm:py-6"
          >
            <div className="max-w-3xl mx-auto">
              {messages.map((msg, i) => (
                <Message
                  key={i}
                  role={msg.role}
                  content={msg.content}
                  citations={msg.citations || []}
                  isNew={i === messages.length - 1 && msg.role === 'assistant'}
                />
              ))}

              {/* Loading indicator */}
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex justify-start mb-4"
                >
                  <div className="bg-[#111827] border border-white/[0.08] rounded-2xl rounded-tl-sm">
                    <LoadingDots />
                  </div>
                </motion.div>
              )}

              <div ref={bottomRef} />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
