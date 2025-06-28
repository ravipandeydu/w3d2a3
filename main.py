"""Tool-Enhanced Reasoning Script.

This script takes natural language queries and uses an LLM to:
1. Interpret the query using chain-of-thought (CoT) style reasoning
2. Call external tools (e.g., a calculator function or string counter) when necessary
3. Combine results to produce a final answer
"""

import os
import re
import json
import openai
from dotenv import load_dotenv

# Import tools
from tools.math_tools import calculate_average, calculate_square_root, perform_comparison
from tools.string_tools import count_vowels, count_letters, count_words

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define available tools
TOOLS = {
    "calculate_average": calculate_average,
    "calculate_square_root": calculate_square_root,
    "perform_comparison": perform_comparison,
    "count_vowels": count_vowels,
    "count_letters": count_letters,
    "count_words": count_words
}

def create_cot_prompt(query):
    """Create a chain-of-thought prompt for the LLM.
    
    Args:
        query (str): The natural language query
        
    Returns:
        str: The prompt for the LLM
    """
    return f"""
    You are an AI assistant that helps solve problems by thinking step by step.
    You have access to the following tools:
    
    - calculate_average(numbers): Calculate the average of a list of numbers
    - calculate_square_root(number): Calculate the square root of a number
    - perform_comparison(a, b, operation): Compare two numbers using the specified operation ('>', '<', '==', '>=', '<=')
    - count_vowels(text): Count the number of vowels in a text
    - count_letters(text): Count the number of letters in a text
    - count_words(text): Count the number of words in a text
    
    For the query: "{query}"
    
    1. Think through the problem step by step
    2. Determine if you need to use any tools
    3. If you need to use a tool, specify which tool and what parameters to use in this format:
       TOOL: <tool_name>(<parameters>)
       For example: TOOL: calculate_average([10, 20])
    4. Provide your final answer
    
    Your response should be structured as follows:
    Reasoning: <your step-by-step reasoning>
    Tool Usage: <tool name and parameters if needed, otherwise 'None'>
    Answer: <your final answer>
    """

def extract_tool_usage(llm_response):
    """Extract tool usage from the LLM response.
    
    Args:
        llm_response (str): The LLM response
        
    Returns:
        tuple: (tool_name, parameters) if a tool is used, (None, None) otherwise
    """
    # Look for the tool usage pattern
    tool_pattern = r"TOOL:\s*([a-zA-Z_]+)\((.+)\)"
    match = re.search(tool_pattern, llm_response)
    
    if match:
        tool_name = match.group(1)
        params_str = match.group(2)
        
        # Parse parameters
        try:
            # Handle list parameters
            if params_str.startswith('[') and params_str.endswith(']'):
                params = eval(params_str)
            # Handle multiple parameters
            elif ',' in params_str:
                params = [eval(p.strip()) for p in params_str.split(',')]
            # Handle single parameter
            else:
                params = eval(params_str)
            
            return tool_name, params
        except Exception as e:
            print(f"Error parsing parameters: {e}")
            return None, None
    
    return None, None

def extract_sections(llm_response):
    """Extract the reasoning, tool usage, and answer sections from the LLM response.
    
    Args:
        llm_response (str): The LLM response
        
    Returns:
        tuple: (reasoning, tool_usage, answer)
    """
    reasoning_match = re.search(r"Reasoning:\s*(.+?)(?=Tool Usage:|$)", llm_response, re.DOTALL)
    tool_usage_match = re.search(r"Tool Usage:\s*(.+?)(?=Answer:|$)", llm_response, re.DOTALL)
    answer_match = re.search(r"Answer:\s*(.+)$", llm_response, re.DOTALL)
    
    reasoning = reasoning_match.group(1).strip() if reasoning_match else ""
    tool_usage = tool_usage_match.group(1).strip() if tool_usage_match else "None"
    answer = answer_match.group(1).strip() if answer_match else ""
    
    return reasoning, tool_usage, answer

def call_llm(prompt):
    """Call the LLM with the given prompt.
    
    Args:
        prompt (str): The prompt for the LLM
        
    Returns:
        str: The LLM response
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that solves problems step by step."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return ""

def process_query(query):
    """Process a natural language query.
    
    Args:
        query (str): The natural language query
        
    Returns:
        dict: The result with reasoning, tool usage, and answer
    """
    # Create the prompt
    prompt = create_cot_prompt(query)
    
    # Call the LLM
    llm_response = call_llm(prompt)
    
    # Extract the reasoning, tool usage, and answer
    reasoning, tool_usage_text, answer = extract_sections(llm_response)
    
    # Extract tool usage
    tool_name, params = extract_tool_usage(llm_response)
    
    # Call the tool if needed
    if tool_name and tool_name in TOOLS:
        try:
            if isinstance(params, list):
                result = TOOLS[tool_name](*params)
            else:
                result = TOOLS[tool_name](params)
            
            # Update the answer with the tool result
            answer = f"{answer} (Tool result: {result})"
        except Exception as e:
            print(f"Error calling tool {tool_name}: {e}")
    
    return {
        "query": query,
        "reasoning": reasoning,
        "tool_usage": tool_usage_text,
        "answer": answer
    }

def main():
    """Main function to run the tool-enhanced reasoning script."""
    print("Tool-Enhanced Reasoning Script")
    print("Enter 'exit' to quit")
    
    while True:
        query = input("\nEnter your query: ")
        
        if query.lower() == "exit":
            break
        
        result = process_query(query)
        
        print("\n===== Result =====")
        print(f"Query: {result['query']}")
        print(f"\nReasoning:\n{result['reasoning']}")
        print(f"\nTool Usage: {result['tool_usage']}")
        print(f"\nAnswer: {result['answer']}")

if __name__ == "__main__":
    main()