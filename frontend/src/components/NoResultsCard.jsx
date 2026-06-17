// Shown when the backend returns an out-of-scope / no-information answer
// Makes the failure case look intentional and polished in demos
import { motion } from 'framer-motion';
import { SearchX } from 'lucide-react';

export function NoResultsCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
      className="
        bg-[#1a1525] border border-amber-500/25 rounded-2xl rounded-tl-sm
        p-4 max-w-[92%] sm:max-w-[78%]
      "
    >
      <div className="flex items-start gap-3">
        {/* Icon */}
        <div className="shrink-0 w-8 h-8 rounded-lg bg-amber-500/10 flex items-center justify-center mt-0.5">
          <SearchX size={15} className="text-amber-400" />
        </div>

        <div className="min-w-0">
          <p className="text-sm font-semibold text-amber-300 mb-1">
            Not found in documents
          </p>
          <p className="text-sm text-gray-400 leading-relaxed">
            I don't have enough information in the provided documents to answer this.
          </p>
          <div className="mt-3 pt-3 border-t border-white/[0.06]">
            <p className="text-xs text-gray-600 italic leading-relaxed">
              💡 Try rephrasing — ask about a specific company (Infosys, Amazon, or Alphabet),
              a specific year, or a specific metric like revenue, margin, or R&D spend.
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
