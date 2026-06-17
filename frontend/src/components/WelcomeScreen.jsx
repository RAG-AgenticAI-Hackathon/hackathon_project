// Welcome / empty state — adapted from frontend_references/ai_assistance_interface/reference_code.txt
// Hero section pattern (PDF Section 6.1): logo + gradient title + subtitle + example chips
import { motion } from 'framer-motion';
import { BarChart2 } from 'lucide-react';
import { EXAMPLE_QUESTIONS, APP_NAME, APP_SUBTITLE } from '../constants';

const chipVariants = {
  hidden: { opacity: 0, y: 10 },
  visible: i => ({
    opacity: 1,
    y: 0,
    transition: { delay: 0.3 + i * 0.08, duration: 0.3, ease: [0.4, 0, 0.2, 1] },
  }),
};

export function WelcomeScreen({ onSelectQuestion }) {
  return (
    <div className="flex flex-col items-center justify-center h-full px-3 sm:px-4 py-6 sm:py-8 text-center overflow-y-auto">

      {/* Logo icon */}
      <motion.div
        initial={{ opacity: 0, scale: 0.85 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4, ease: [0.4, 0, 0.2, 1] }}
        className="mb-5"
      >
        <div className="
          w-16 h-16 rounded-2xl mx-auto mb-4 flex items-center justify-center
          bg-gradient-to-br from-blue-600 to-purple-700
          shadow-[0_0_40px_rgba(124,58,237,0.35)]
        ">
          <BarChart2 size={28} className="text-white" />
        </div>

        {/* Gradient app title (PDF Section 5.4) */}
        <h1
          className="text-2xl sm:text-3xl font-bold font-display tracking-tight"
          style={{
            background: 'linear-gradient(135deg, #60A5FA 0%, #A78BFA 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
          }}
        >
          {APP_NAME}
        </h1>

        <p className="mt-2 text-xs sm:text-sm text-gray-500 max-w-xs sm:max-w-sm mx-auto leading-relaxed">
          {APP_SUBTITLE}
        </p>
      </motion.div>

      {/* Company tags */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2, duration: 0.3 }}
        className="flex items-center gap-2 mb-8 flex-wrap justify-center"
      >
        {['Infosys', 'Amazon', 'Alphabet'].map(c => (
          <span key={c} className="text-xs text-gray-600 border border-white/[0.08] px-3 py-1 rounded-full">
            {c}
          </span>
        ))}
      </motion.div>

      {/* Example question chips — staggered fade-in (command suggestions from ai_assistance_interface reference) */}
      <div className="w-full max-w-lg space-y-2 pb-4">
        <p className="text-[11px] text-gray-700 uppercase tracking-widest mb-3">Try asking</p>

        {EXAMPLE_QUESTIONS.map((q, i) => (
          <motion.button
            key={i}
            custom={i}
            variants={chipVariants}
            initial="hidden"
            animate="visible"
            onClick={() => onSelectQuestion(q)}
            className="
              w-full text-left px-4 py-3 rounded-xl text-sm text-gray-400
              bg-[#111827] border border-white/[0.07]
              hover:border-blue-500/40 hover:bg-[#141e30] hover:text-gray-200
              transition-all duration-200
            "
          >
            {q}
          </motion.button>
        ))}
      </div>
    </div>
  );
}
