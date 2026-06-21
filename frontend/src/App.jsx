// Dark Luxury theme (PDF Section 1.6) + 60-30-10 color rule (PDF Section 5.3)
// 60% = #0D0D1A background, 30% = #111827 cards, 10% = #2563EB accent
import { useState, useCallback } from 'react';
import { BarChart2 } from 'lucide-react';
import { ChatWindow } from './components/ChatWindow';
import { ChatInput } from './components/ChatInput';
import { CompanySelector } from './components/CompanySelector';
import { askQuestion } from './api/chat';
import { APP_NAME } from './constants';

export default function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [company, setCompany] = useState('All'); // 'All' = compare across all reports

  const handleSubmit = useCallback(async (question) => {
    const userMsg = { role: 'user', content: question, citations: [] };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const data = await askQuestion(question, company);
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: data.answer,
          citations: data.citations || [],
          questionType: data.question_type,
        },
      ]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: "Couldn't reach the backend. Make sure the server is running at localhost:8000 and try again.",
          citations: [],
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }, [company]);

  return (
    <div className="h-screen flex flex-col bg-[#0D0D1A] relative overflow-hidden">

      {/* Background glow orbs — subtle depth effect */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden z-0">
        <div
          className="absolute -top-32 left-1/2 -translate-x-1/2 w-[700px] h-[400px] rounded-full opacity-[0.12]"
          style={{ background: '#7C3AED', filter: 'blur(80px)' }}
        />
        <div
          className="absolute bottom-0 right-0 w-[400px] h-[400px] rounded-full opacity-[0.07]"
          style={{ background: '#2563EB', filter: 'blur(80px)' }}
        />
      </div>

      {/* Header */}
      <header className="relative z-10 shrink-0 px-6 py-4 border-b border-white/[0.07] flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-700 flex items-center justify-center shadow-[0_0_16px_rgba(124,58,237,0.4)]">
            <BarChart2 size={16} className="text-white" />
          </div>
          <span
            className="text-lg font-bold font-display tracking-tight"
            style={{
              background: 'linear-gradient(135deg, #60A5FA 0%, #A78BFA 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
            }}
          >
            {APP_NAME}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <span className="hidden sm:flex text-[11px] text-gray-600 border border-white/[0.07] px-3 py-1 rounded-full">
            Infosys · Amazon · Alphabet
          </span>
          {isLoading && (
            <span className="text-[11px] text-blue-400 animate-pulse">Thinking…</span>
          )}
        </div>
      </header>

      {/* Chat area */}
      <ChatWindow
        messages={messages}
        isLoading={isLoading}
        onSelectQuestion={handleSubmit}
      />

      {/* Company scope selector + input bar */}
      <div className="relative z-10">
        <div className="px-6 pt-3 flex items-center gap-3">
          <span className="text-[11px] text-gray-600 shrink-0">Scope:</span>
          <CompanySelector selected={company} onSelect={setCompany} />
        </div>
        <ChatInput onSubmit={handleSubmit} isLoading={isLoading} />
      </div>
    </div>
  );
}
