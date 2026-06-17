// Adapted from frontend_references/user_message_reference_code.txt (InputBar component)
// Key parts: auto-resize textarea, Enter to submit, idle/typing/loading send button states
import { useState, useRef, useEffect, useCallback } from 'react';
import { ArrowUp, Square } from 'lucide-react';

export function ChatInput({ onSubmit, isLoading }) {
  const [input, setInput] = useState('');
  const textareaRef = useRef(null);

  // Auto-resize textarea as user types (from InputBar reference)
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = '0';
    const next = Math.min(el.scrollHeight, 120);
    el.style.height = `${next}px`;
    el.style.overflowY = el.scrollHeight > 120 ? 'auto' : 'hidden';
  }, [input]);

  const handleSubmit = useCallback(() => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;
    onSubmit(trimmed);
    setInput('');
  }, [input, isLoading, onSubmit]);

  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }, [handleSubmit]);

  const hasInput = input.trim().length > 0;

  // Button state: idle | typing | loading
  const btnActive = (hasInput && !isLoading) || isLoading;

  return (
    <div className="shrink-0 px-3 sm:px-4 pb-4 sm:pb-5 pt-2 border-t border-white/[0.06]">
      <div className="mx-auto max-w-3xl">
        {/* Input container — styled from InputBar reference */}
        <div
          className="relative rounded-2xl bg-[#111827] border border-white/[0.08] shadow-sm transition-colors focus-within:border-white/[0.18]"
        >
          <div className="pt-3 pb-0 pr-3 pl-4 min-h-[44px]">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about Infosys, Amazon, or Alphabet..."
              disabled={isLoading}
              rows={1}
              className="
                w-full resize-none bg-transparent border-0 outline-none
                text-[14px] leading-[1.6] text-[#F1F1EE]
                placeholder:text-gray-600
                overflow-hidden disabled:opacity-40
              "
            />
          </div>

          <div className="flex items-center justify-between px-3 pt-1 pb-2.5">
            {/* Hint */}
            <span className="text-[11px] text-gray-700 hidden sm:block">
              Shift+Enter for new line
            </span>

            {/* Send / stop button */}
            <button
              onClick={isLoading ? undefined : handleSubmit}
              disabled={!hasInput && !isLoading}
              aria-label={isLoading ? 'Waiting...' : 'Send'}
              className={`
                inline-flex items-center justify-center w-8 h-8 rounded-full
                transition-all duration-150
                ${btnActive
                  ? 'bg-blue-600 text-white hover:bg-blue-500 shadow-[0_0_16px_rgba(37,99,235,0.4)]'
                  : 'bg-white/10 text-gray-600 cursor-not-allowed'
                }
              `}
            >
              {isLoading
                ? <Square size={10} fill="currentColor" />
                : <ArrowUp size={14} />
              }
            </button>
          </div>
        </div>

        <p className="text-center text-[11px] text-gray-700 mt-2">
          Answers grounded in annual reports only — not financial advice.
        </p>
      </div>
    </div>
  );
}
