# Tool-Enhanced Reasoning Script

This project implements a Python script that takes natural language queries and uses an LLM to interpret the query, call external tools when necessary, and combine results to produce a final answer.

## Features

- Chain-of-thought (CoT) style reasoning using OpenAI's GPT models
- Automatic tool selection based on query requirements
- Support for mathematical operations and string analysis
- Detailed output showing reasoning steps, tool usage, and final answers

## Project Structure

```
├── main.py                # Main script that processes queries
├── tools/                 # Directory containing tool implementations
│   ├── math_tools.py      # Mathematical operations tools
│   └── string_tools.py    # String analysis tools
├── .env.example           # Example environment variables file
└── requirements.txt       # Project dependencies
```

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Copy the `.env.example` file to `.env`
   - Replace `your_openai_api_key_here` with your actual OpenAI API key

## Usage

Run the script using Python:

```
python main.py
```

Enter your natural language query when prompted. Type `exit` to quit the program.

## Example Queries and Output

### Example 1: Mathematical Operation

**Query:** "What's the square root of the average of 18 and 50?"

**Output:**
```
Reasoning:
To find the square root of the average of 18 and 50, I need to:
1. Calculate the average of 18 and 50: (18 + 50) / 2 = 68 / 2 = 34
2. Calculate the square root of 34: √34 ≈ 5.83

I'll need to use tools for these calculations.

Tool Usage: calculate_average([18, 50]) followed by calculate_square_root(34)

Answer: The square root of the average of 18 and 50 is approximately 5.83.
```

### Example 2: String Analysis

**Query:** "How many vowels are in the word 'Multimodality'?"

**Output:**
```
Reasoning:
To count the vowels in 'Multimodality', I need to identify all the vowels (a, e, i, o, u) in the word.
The vowels in 'Multimodality' are: u, i, o, a, i

I'll use a tool to count these vowels.

Tool Usage: count_vowels("Multimodality")

Answer: There are 5 vowels in the word 'Multimodality'.
```

### Example 3: Comparison

**Query:** "Is the number of letters in 'machine' greater than the number of vowels in 'reasoning'?"

**Output:**
```
Reasoning:
To answer this question, I need to:
1. Count the number of letters in 'machine': m, a, c, h, i, n, e = 7 letters
2. Count the number of vowels in 'reasoning': e, a, o, i = 4 vowels
3. Compare if 7 > 4

I'll use tools for these calculations.

Tool Usage: perform_comparison(count_letters("machine"), count_vowels("reasoning"), ">")

Answer: Yes, the number of letters in 'machine' (7) is greater than the number of vowels in 'reasoning' (4).
```

### Example 4: Complex Calculation

**Query:** "What is the average number of vowels in the words 'artificial', 'intelligence', and 'programming'?"

**Output:**
```
Reasoning:
To find the average number of vowels in these words, I need to:
1. Count the vowels in 'artificial': a, i, i, i, a = 5 vowels
2. Count the vowels in 'intelligence': i, e, i, e, e = 5 vowels
3. Count the vowels in 'programming': o, a, i = 3 vowels
4. Calculate the average: (5 + 5 + 3) / 3 = 13 / 3 ≈ 4.33

I'll use tools for these calculations.

Tool Usage: calculate_average([count_vowels("artificial"), count_vowels("intelligence"), count_vowels("programming")])

Answer: The average number of vowels in the words 'artificial', 'intelligence', and 'programming' is approximately 4.33.
```

### Example 5: Multi-step Analysis

**Query:** "Is the square root of the number of letters in 'computational' less than the number of vowels in 'intelligence'?"

**Output:**
```
Reasoning:
To answer this question, I need to:
1. Count the number of letters in 'computational': c, o, m, p, u, t, a, t, i, o, n, a, l = 13 letters
2. Calculate the square root of 13: √13 ≈ 3.61
3. Count the number of vowels in 'intelligence': i, e, i, e, e = 5 vowels
4. Compare if 3.61 < 5

I'll use tools for these calculations.

Tool Usage: perform_comparison(calculate_square_root(count_letters("computational")), count_vowels("intelligence"), "<")

Answer: Yes, the square root of the number of letters in 'computational' (√13 ≈ 3.61) is less than the number of vowels in 'intelligence' (5).
```

## How the Prompt Helps Decide Tool Usage

The prompt is designed to guide the LLM through a structured reasoning process that helps it determine when and which tools to use. Here's how it works:

1. **Clear Tool Descriptions**: The prompt provides clear descriptions of all available tools, making it easy for the LLM to understand their functionality.

2. **Step-by-Step Reasoning**: By asking the LLM to "Think through the problem step by step," it encourages a methodical approach that breaks down complex queries into simpler operations.

3. **Explicit Tool Usage Format**: The prompt specifies a clear format for tool usage (`TOOL: <tool_name>(<parameters>)`), making it easy to parse the LLM's response and extract tool calls.

4. **Structured Response Format**: By requiring the LLM to structure its response with clear sections (Reasoning, Tool Usage, Answer), it becomes easier to extract and process each component.

5. **Low Temperature Setting**: The script uses a low temperature setting (0.2) when calling the OpenAI API, which encourages more deterministic and logical responses, improving the accuracy of tool selection.

This approach allows the script to effectively determine when a tool is needed based on the nature of the query and the LLM's reasoning process, without requiring complex frameworks or agents.