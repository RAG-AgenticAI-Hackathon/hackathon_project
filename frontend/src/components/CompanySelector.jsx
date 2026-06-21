// Horizontal toggle pills to scope questions to a company (or All / Compare).
// Active company pills reuse COMPANY_BADGE colors from constants/index.js.
import { motion } from 'framer-motion';
import { COMPANY_BADGE } from '../constants';

// 'All' = default, no scoping (Compare across all reports)
const OPTIONS = ['All', 'Infosys', 'Amazon', 'Alphabet'];

const LABELS = { All: 'All / Compare' };

export function CompanySelector({ selected = 'All', onSelect }) {
  return (
    <div className="flex items-center gap-1.5 flex-wrap">
      {OPTIONS.map((opt) => {
        const isActive = selected === opt;
        const badge = COMPANY_BADGE[opt]; // undefined for 'All'

        // Active styling: company badge colors, or accent blue for All / Compare
        const activeClass = badge
          ? `${badge.bg} ${badge.text}`
          : 'bg-blue-600 text-white';

        return (
          <motion.button
            key={opt}
            type="button"
            onClick={() => onSelect?.(opt)}
            whileTap={{ scale: 0.96 }}
            className={`px-3 py-1 rounded-full text-[11px] font-semibold transition-colors ${
              isActive
                ? activeClass
                : 'bg-white/[0.04] text-gray-400 border border-white/[0.08] hover:bg-white/[0.08] hover:text-gray-200'
            }`}
          >
            {LABELS[opt] || opt}
          </motion.button>
        );
      })}
    </div>
  );
}
