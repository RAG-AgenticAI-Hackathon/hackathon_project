// Message bubble — fade-up on mount (PDF §2.2), word-by-word reveal (PDF §2.5)
// Automatically switches to NoResultsCard when backend says "not enough information"
import { useRef, useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { CitationCard } from './CitationCard';
import { NoResultsCard } from './NoResultsCard';

// Phrases the backend uses when a question is out of scope
const OUT_OF_SCOPE_PHRASES = [
  "i don't have enough information",
  "i do not have enough information",
  "not enough information in the provided documents",
  "cannot answer this",
  "can't answer this",
  "outside the scope",
  "not covered in the",
];

function isOutOfScope(text) {
  const lower = (text || '').toLowerCase();
  return OUT_OF_SCOPE_PHRASES.some(p => lower.includes(p));
}

export function Message({ role, content, citations = [], isNew = false }) {
  const isUser = role === 'user';
  const outOfScope = !isUser && isOutOfScope(content);

  // Capture isNew at mount — avoids re-triggering animation when prop changes
  const isNewRef = useRef(isNew);

  const [displayedWords, setDisplayedWords] = useState(() =>
    isNewRef.current && !isUser && !outOfScope ? [] : content.split(' ')
  );

  // Word-by-word reveal for new assistant messages
  useEffect(() => {
    if (!isNewRef.current || isUser || outOfScope) return;

    const wordList = content.split(' ');
    let i = 0;
    const interval = setInterval(() => {
      i++;
      setDisplayedWords(wordList.slice(0, i));
      if (i >= wordList.length) clearInterval(interval);
    }, 35);

    return () => clearInterval(interval);
  }, []); // runs once on mount

  return (
    <motion.div
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.28, ease: [0.4, 0, 0.2, 1] }}
      className={`flex mb-5 ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div className={`max-w-[92%] sm:max-w-[78%] ${isUser ? 'items-end' : 'items-start'} flex flex-col`}>
        {/* Role label */}
        <p className={`text-[11px] text-gray-600 mb-1 ${isUser ? 'text-right' : 'text-left'}`}>
          {isUser ? 'You' : 'FinSight'}
        </p>

        {/* Out-of-scope → styled card instead of plain bubble */}
        {outOfScope ? (
          <NoResultsCard />
        ) : (
          <div
            className={`px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap break-words ${
              isUser
                ? 'bg-blue-600 text-white rounded-tr-sm'
                : 'bg-[#111827] text-[#F1F1EE] border border-white/[0.08] rounded-tl-sm'
            }`}
          >
            {isUser ? content : displayedWords.join(' ')}
          </div>
        )}

        {/* Source count pill */}
        {!isUser && !outOfScope && citations.length > 0 && (
          <span className="mt-1.5 text-[10px] text-gray-600">
            {citations.length} source{citations.length > 1 ? 's' : ''} retrieved
          </span>
        )}

        {/* Citation accordion cards */}
        {!isUser && !outOfScope && citations.length > 0 && (
          <div className="mt-2 w-full space-y-1.5">
            {citations.map((c, i) => (
              <CitationCard key={i} {...c} />
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}
