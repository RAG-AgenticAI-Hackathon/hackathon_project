// Adapted from frontend_references/badge/ref_code.txt
// Colors from frontend_references/badge/colors.txt: all subtle variants
import { COMPANY_BADGE } from '../constants';

export function CompanyBadge({ company }) {
  const style = COMPANY_BADGE[company];
  if (!style) {
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-gray-200 text-gray-800">
        {company}
      </span>
    );
  }
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${style.bg} ${style.text}`}>
      {company}
    </span>
  );
}
