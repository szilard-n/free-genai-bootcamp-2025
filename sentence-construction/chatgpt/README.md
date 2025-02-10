# ChatGPT Assistant Guide

## Which Model

GPT-4-turbo (free version)

## Prompting Guide

https://platform.openai.com/docs/guides/prompt-engineering

A good prompting guide for the currently used GPT model (GPT-4-turbo) depends on the complexity of the task, but here are some best practices for getting optimal results:

1. Be Clear and Specific
	•	Avoid vague prompts like:
“Tell me about Java.”
	•	Instead, be precise:
“Explain the differences between Java 8 and Java 17, focusing on performance improvements and new language features.”

2. Provide Context and Constraints
	•	Instead of:
“Give me a LinkedIn bio.”
	•	Try:
“Write a professional LinkedIn bio for a senior Java backend engineer with 6 years of experience in Spring Boot, Quarkus, and cloud infrastructure. Keep it concise and formal, emphasizing freelancing and contracting experience.”

3. Use Step-by-Step or Structured Prompts

If you’re asking for something complex, break it down.
	•	Instead of:
“Explain machine learning.”
	•	Try:
“Explain machine learning in three parts: (1) What it is, (2) How it works, and (3) Real-world applications. Keep it concise and easy to understand.”

4. Format Requests for Code & Technical Queries

If you need code, specify language, framework, and constraints.
	•	Instead of:
“Write a Java function to sort a list.”
	•	Try:
“Write a Java function using Streams to sort a List<String> in descending order. Ensure it is efficient and avoids modifying the original list.”

5. Use Role-Based Prompting for Best Results
	•	“You are a senior Java developer. Explain the best practices for securing REST APIs in Spring Boot.”
	•	“You are a technical recruiter. Write an engaging LinkedIn post about hiring backend engineers with cloud experience.”

6. Use Examples When Possible
	•	“Write an email template for reaching out to potential clients on LinkedIn. Example tone: ‘Hi [Name], I saw that you’re hiring for a backend role…’ Keep it friendly yet professional.”

7. Define Output Format (Lists, Tables, JSON, Markdown, etc.)

If you need structured output:
	•	“Provide the response as a Markdown table.”
	•	“Give me a JSON object with keys: ‘title’, ‘description’, and ‘keywords’ for an SEO article.”

Example JSON request:

{
  "title": "Optimizing Spring Boot Performance",
  "description": "A detailed guide on tuning Spring Boot for high performance.",
  "keywords": ["Spring Boot", "Performance", "Java Optimization"]
}

8. Iterative Refinement

If the first result isn’t perfect, refine it:
	•	“Make it more concise.”
	•	“Rewrite this to sound more engaging.”
	•	“Improve clarity and structure.”

9. Few-Shot Learning (Provide Examples for Better Output)

If you want GPT to follow a pattern:
	•	“Here are two example LinkedIn posts. Write a third one in the same style.”
	•	“Given these two well-structured explanations, write a similar one about Kubernetes.”

10. Avoid Open-Ended or Ambiguous Requests
	•	Instead of:
“Tell me something interesting.”
	•	Try:
“Tell me an interesting fact about AI advancements in 2024.”