# Claude Assistant Guide

## Which Model

Claude 3.5 Sonnet (premium version)

## Prompt Engineering Guide for Claude 3.5 Sonnet

### Core Principles

1. **Clarity and Specificity**
   - Be explicit about your desired outcome and format
   - Include all relevant context upfront
   - Break complex requests into smaller, manageable parts

2. **Structured Data Formats**
   - XML is excellent for hierarchical data and complex structures
   - JSON works well for data organization and API-like interactions
   - Markdown is preferred for text formatting and documentation

### Best Practices

#### Use Clear Task Descriptions

```markdown
Bad: "Make this better"
Good: "Please revise this email to be more professional while maintaining its core message about project delays"
```

#### Leverage XML for Complex Instructions

```xml
<task>
    <objective>Create a marketing plan</objective>
    <constraints>
        <budget>50000</budget>
        <timeline>3 months</timeline>
    </constraints>
    <requirements>
        <focus>Social media</focus>
        <target_audience>Young professionals</target_audience>
    </requirements>
</task>
```

#### Structure Multi-Part Requests

```markdown
1. First, analyze the current market data
2. Then, identify key trends
3. Finally, provide recommendations based on findings
```

### Advanced Techniques

#### Temperature Control
- Be explicit about creativity needs:
  - For creative tasks: "Please be creative and provide multiple unique approaches"
  - For technical tasks: "Please provide precise, factual information only"

#### Context Windows
- Front-load important information
- Group related information together
- Use clear section breaks for different types of input

#### Output Format Control

Use explicit format requests:

```markdown
Please provide the response in this structure:
1. Executive Summary (2-3 sentences)
2. Detailed Analysis
   - Key findings
   - Supporting data
3. Recommendations
```

### Common Patterns

#### For Analysis Tasks
```markdown
Given [specific input/data],
Please analyze:
1. [aspect 1]
2. [aspect 2]
3. [aspect 3]
Provide conclusions focusing on [specific angles]
```

#### For Creative Tasks
```markdown
Context: [background information]
Task: Create [specific output]
Requirements:
- [requirement 1]
- [requirement 2]
Style: [tone/voice preferences]
Format: [desired structure]
```

### Troubleshooting

If you're not getting desired results:

1. Add more specific constraints
2. Break down complex requests into smaller steps
3. Use example inputs and outputs
4. Specify the exact format you want for the output

### Special Considerations

#### Data Processing
When working with data, specify:
- Input format
- Desired transformations
- Expected output format
- Error handling preferences

#### Interactive Sessions
For multi-turn conversations:
- Reference previous context explicitly
- Build on previous responses
- Use clear transition markers between different parts of the conversation

Remember: Claude 3.5 Sonnet excels at handling complex, nuanced tasks when given clear, structured instructions. The more specific and well-organized your prompt, the better the output quality will be.

For detailed documentation and updates, you can visit Anthropic's documentation at https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview