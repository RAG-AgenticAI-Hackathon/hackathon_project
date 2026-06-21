// Set MOCK_MODE = true to test the full UI without needing the backend running.
// Flip back to false once Person B's API is up at localhost:8000.
const MOCK_MODE = false;

const API_BASE =
  import.meta.env.VITE_API_URL ||
  "https://unnoticed-overwrite-prior.ngrok-free.dev";

// Mock responses 

const MOCK_SIMPLE = {
  answer:
    "Infosys reported a net revenue of ₹1,46,767 crore (approximately $18.2 billion USD) for FY2024, representing a 20.7% growth in reported currency terms compared to the previous year. The digital segment accounted for 62.5% of total revenues.",
  citations: [
    {
      company: "Infosys",
      year: 2024,
      similarity: 0.92,
      preview:
        "For the year ended March 31, 2024, the Company reported revenues of ₹146,767 crores, a growth of 20.7% in reported currency terms and 16.0% in constant currency terms over the prior year.",
    },
    {
      company: "Infosys",
      year: 2024,
      similarity: 0.84,
      preview:
        "The digital segment continued to be the primary growth driver, accounting for 62.5% of total revenues. Large deal wins during the year totalled $9.8 billion.",
    },
  ],
  question_type: "SIMPLE",
};

const MOCK_COMPLEX = {
  answer:
    "**Infosys:**\nInfosys reported an operating margin of 20.7% for FY2024, slightly lower than 22.0% in FY2023, primarily due to higher employee costs and investments in talent.\n\n**Amazon:**\nAmazon's consolidated operating margin was 6.4% for FY2023, recovering strongly from near-zero margins in 2022. AWS alone contributed an operating margin of 28.9%, offsetting thinner margins in retail.",
  citations: [
    {
      company: "Infosys",
      year: 2024,
      similarity: 0.91,
      preview: "Operating margin for the year was 20.7% as compared to 22.0% in FY2023, impacted by wage revision cycles and strategic hiring.",
    },
    {
      company: "Infosys",
      year: 2024,
      similarity: 0.79,
      preview: "Employee benefit expenses grew by 14.2% year-over-year, primarily driven by merit increases and variable pay.",
    },
    {
      company: "Amazon",
      year: 2023,
      similarity: 0.88,
      preview: "Operating income was $36.9 billion, compared to an operating loss of $2.5 billion in 2022. AWS operating income was $22.4 billion with a margin of 28.9%.",
    },
    {
      company: "Amazon",
      year: 2023,
      similarity: 0.76,
      preview: "North America segment operating margin improved to 3.6% from a loss position in 2022, driven by lower fulfilment costs per unit.",
    },
  ],
  question_type: "COMPLEX",
};

const MOCK_OUT_OF_SCOPE = {
  answer:
    "I don't have enough information in the provided documents to answer this. The question may be outside the scope of the Infosys, Amazon, and Alphabet annual reports available in the system.",
  citations: [],
  question_type: "SIMPLE",
};

/** Pick a mock response based on simple keyword matching */
function getMockResponse(question) {
  const q = question.toLowerCase();

  // Out-of-scope keywords
  const financeTerms = /infosys|amazon|alphabet|google|revenue|profit|margin|r&d|research|employee|segment|operating|income|cash|debt|dividend|eps|growth|quarter|annual|fy20|fy21|fy22|fy23|fy24/;
  if (!financeTerms.test(q)) return MOCK_OUT_OF_SCOPE;

  // Multi-company = COMPLEX
  const companies = ['infosys', 'amazon', 'alphabet', 'google'];
  const mentioned = companies.filter(c => q.includes(c));
  const compareWords = /compare|vs|versus|both|difference|between|which|higher|lower|better|more|less/;
  if (mentioned.length >= 2 || compareWords.test(q)) return MOCK_COMPLEX;

  return MOCK_SIMPLE;
}

// ─── Real or mock fetch ───────────────────────────────────────────────────────

export async function askQuestion(query, company) {
  // 'All' (or empty) = no scoping. Otherwise prepend a light hint so scoping
  // works in the demo even before the backend reads the `company` field.
  const isScoped = company && company !== 'All';
  const scopedQuery = isScoped ? `[Scope: ${company}] ${query}` : query;

  if (MOCK_MODE) {
    // Simulate network delay
    await new Promise(r => setTimeout(r, 1200 + Math.random() * 800));
    return getMockResponse(scopedQuery);
  }

  const response = await fetch(`${API_BASE}/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    // `company` is optional/non-breaking — backend can ignore it for now.
    body: JSON.stringify({ question: scopedQuery, company: isScoped ? company : null }),
  });

  if (!response.ok) {
    throw new Error(`Server error ${response.status}`);
  }

  return response.json();
}
