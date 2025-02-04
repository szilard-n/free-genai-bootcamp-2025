# DeepSeek Assistant Guide

## Which Model
Mixture-of-Experts (MoE) language model with 671B total parameters with 37B activated for each token

## Promting Guide

For **DeepSeek-V3**, the format that provides better context depends on the task and the type of information you want the model to process. While DeepSeek-V3 is highly flexible and can work with various formats (plain text, JSON, XML, etc.), the key to providing better context lies in **clarity, structure, and consistency** rather than relying on a specific format. Below are some recommendations for optimizing context:

---

### 1. **Use Clear and Structured Plain Text**
   - Plain text with clear headings, labels, and separators is often sufficient for providing context.
   - Use **markers** like `###`, `**`, or `---` to distinguish between different parts of the prompt (e.g., instructions, examples, input/output pairs).

   **Example:**
   ```
   ### Task:
   Translate the following English phrases to Spanish.

   ### Examples:
   **Input:** Good morning
   **Output:** Buenos días

   **Input:** How are you?
   **Output:** ¿Cómo estás?

   ### New Input:
   **Input:** What is your name?
   **Output:**
   ```

   This format is simple and works well for most tasks.

---

### 2. **Use Key-Value Pairs (JSON-like Structure)**
   - If your task involves structured data or requires the model to handle multiple inputs/outputs, a **key-value pair** format can help provide better context.
   - DeepSeek-V3 can interpret this structure effectively.

   **Example:**
   ```
   Task: Translate English phrases to Spanish.

   Examples:
   - Input: "Good morning"
     Output: "Buenos días"
   - Input: "How are you?"
     Output: "¿Cómo estás?"

   New Input:
   - Input: "What is your name?"
     Output:
   ```

   This format is particularly useful for tasks involving multiple attributes or parameters.

---

### 3. **Use Step-by-Step Instructions**
   - Break down complex tasks into smaller steps and provide context for each step.
   - This helps the model understand the sequence of actions or reasoning required.

   **Example:**
   ```
   ### Task:
   Solve the following math problem step by step.

   ### Problem:
   What is 25% of 80?

   ### Steps:
   1. Convert 25% to a decimal: 25% = 0.25
   2. Multiply 0.25 by 80: 0.25 * 80 = 20

   ### Answer:
   20
   ```

   This approach is ideal for tasks requiring logical reasoning or multi-step processes.

---

### 4. **Use Role-Playing or Persona-Based Context**
   - If the task involves role-playing or requires the model to adopt a specific tone or perspective, explicitly define the role or persona in the prompt.
   - This helps the model align its responses with the desired context.

   **Example:**
   ```
   ### Role:
   You are a customer support agent for an online store. Respond to the customer's query in a polite and helpful manner.

   ### Customer Query:
   "My order hasn't arrived yet. Can you help me?"

   ### Response:
   "I apologize for the delay. Could you please provide your order number so I can check the status for you?"
   ```

   This format is useful for conversational or role-specific tasks.

---

### 5. **Use XML or JSON for Structured Data (Optional)**
   - While DeepSeek-V3 doesn't specifically optimize for XML or JSON, these formats can still be used if your task involves highly structured data.
   - Ensure the structure is simple and easy to parse.

   **Example (XML):**
   ```xml
   <task>
       <description>Translate English phrases to Spanish</description>
       <examples>
           <example>
               <input>Good morning</input>
               <output>Buenos días</output>
           </example>
           <example>
               <input>How are you?</input>
               <output>¿Cómo estás?</output>
           </example>
       </examples>
       <new_input>
           <input>What is your name?</input>
           <output></output>
       </new_input>
   </task>
   ```

   **Example (JSON):**
   ```json
   {
     "task": "Translate English phrases to Spanish",
     "examples": [
       {
         "input": "Good morning",
         "output": "Buenos días"
       },
       {
         "input": "How are you?",
         "output": "¿Cómo estás?"
       }
     ],
     "new_input": {
       "input": "What is your name?",
       "output": ""
     }
   }
   ```

   These formats are useful for tasks involving APIs, data extraction, or integration with other systems.

---

### 6. **Use Few-Shot Learning with Examples**
   - Provide a few examples (2–5) to demonstrate the task. This helps the model understand the pattern and generate accurate responses.
   - Ensure the examples are diverse and cover different scenarios.

   **Example:**
   ```
   ### Task:
   Classify the sentiment of the following text as "Positive," "Negative," or "Neutral."

   ### Examples:
   **Text:** "I love this product! It works perfectly."
   **Sentiment:** Positive

   **Text:** "The service was slow and unhelpful."
   **Sentiment:** Negative

   **Text:** "The package arrived on time."
   **Sentiment:** Neutral

   ### New Text:
   **Text:** "The movie was okay, but the ending was disappointing."
   **Sentiment:**
   ```

---

### 7. **Use Explicit Instructions for Ambiguity**
   - If the task involves ambiguous inputs, provide explicit instructions on how to handle them.
   - This reduces the likelihood of the model generating incorrect or inconsistent responses.

   **Example:**
   ```
   ### Task:
   Answer the following questions. If the question is unclear or cannot be answered, respond with "I don't know."

   ### Examples:
   **Question:** What is the capital of France?
   **Answer:** Paris

   **Question:** How tall is the Eiffel Tower?
   **Answer:** I don't know.

   ### New Question:
   **Question:** What is the meaning of life?
   **Answer:**
   ```

---

### Key Takeaways:
- **Clarity and structure** are more important than the specific format.
- Use **plain text with clear markers** for most tasks.
- For structured data, **JSON or XML** can be used, but keep the structure simple.
- Provide **examples, step-by-step instructions, or role-based context** to guide the model effectively.

By following these guidelines, you can provide better context for DeepSeek-V3 and improve its performance on your specific tasks.

# Prompting Journey Notes

- DeepSeek is correctly respecting the given rules and constraints
- DeepSeek server is always busy and it takes a lot of retries to respond
- Retrying the promts many time results to error messages stating that there were too many requests and that I should wait.