// Adapted from card hover pattern (PDF Section 6.6) + accordion pattern (Section 6.4)
// Used to show retrieved source documents below each answer
import { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { CompanyBadge } from './Badge';

export function CitationCard({ company, year, similarity, preview }) {
  const [expanded, setExpanded] = useState(false);

  const matchPct = similarity != null ? `${Math.round(similarity * 100)}% match` : null;

  return (
    <div
      onClick={() => setExpanded(v => !v)}
      className="
        bg-[#111827] border border-white/[0.08] rounded-xl p-3 cursor-pointer
        transition-all duration-250
        hover:-translate-y-[2px] hover:shadow-[0_8px_24px_rgba(0,0,0,0.4)] hover:border-white/[0.14]
      "
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 flex-wrap">
          <CompanyBadge company={company} />
          {year && <span className="text-xs text-gray-500">{year}</span>}
          {matchPct && <span className="text-xs text-gray-600">· {matchPct}</span>}
        </div>
        <ChevronDown
          size={14}
          className={`text-gray-600 shrink-0 transition-transform duration-300 ${expanded ? 'rotate-180' : ''}`}
        />
      </div>

      {/* Accordion body — Section 6.4 pattern */}
      <div
        className="overflow-hidden transition-all duration-300 ease-in-out"
        style={{ maxHeight: expanded ? '160px' : '0px' }}
      >
        <p className="mt-2 text-xs text-gray-400 italic leading-relaxed line-clamp-5">
          {preview || 'No preview available.'}
        </p>
      </div>
    </div>
  );
}
