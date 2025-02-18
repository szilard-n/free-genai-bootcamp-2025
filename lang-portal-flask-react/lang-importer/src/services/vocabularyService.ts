import { GenerateVocabularyParams } from '@/types/vocabulary';

const GROQ_API_URL = import.meta.env.VITE_GROQ_API_URL;
const GROQ_API_KEY = import.meta.env.VITE_GROQ_API_KEY;

export async function generateVocabulary({ theme, count }: GenerateVocabularyParams): Promise<string> {
    const prompt = `Generate a structured JSON output for German vocabulary related to the theme ${theme}. The response should be a structured JSON like the following example:

[
  {
    "english": "cheap",
    "german": "billig"
  },
  {
    "english": "large",
    "german": "groß"
  }
]

Generate ${count} vocabulary items and send back raw JSON and nothing else.`

  try {
    const response = await fetch(GROQ_API_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${GROQ_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: [{
          role: 'user',
          content: prompt
        }],
        model: 'gemma2-9b-it',
      }),
    });

    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('API error details:', errorText);
      throw new Error(`API request failed with status ${response.status}: ${errorText}`);
    }

    const data = await response.json();
    const content = data.choices[0]?.message?.content;

    if (!content) {
      throw new Error('No content received from API');
    }

    return content;

  } catch (error) {
    console.error('Detailed error in generateVocabulary:', error);
    throw error;
  }
} 