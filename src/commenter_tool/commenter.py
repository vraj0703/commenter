import sys
import os
import subprocess
import time
import re
import textwrap # NEW: Import the textwrap module

# --- Configuration ---
OLLAMA_MODEL = "llama3"

# --- Main Script Logic ---
# NEW: Function to enforce the 80-character line limit
def rewrap_comment_block(comment_block: str, width: int = 80) -> str:
    """
    Re-wraps a comment block to a specified width, preserving comment prefixes.

    Args:
        comment_block: The multi-line string representing the comment block.
        width: The maximum line width.

    Returns:
        The reformatted comment block as a single string.
    """
    reformatted_lines = []

    # Heuristic to find the content-bearing lines (ignores lines like /** or */)
    def is_content_line(line):
        return re.search(r'[a-zA-Z0-9]', line)

    for line in comment_block.splitlines():
        if len(line) <= width or not is_content_line(line):
            reformatted_lines.append(line)
            continue

        # Find the indentation and comment prefix (e.g., " * " or "# ")
        match = re.match(r'^(\s*[\*#/]*\s*)', line)
        prefix = match.group(1) if match else ''
        content = line[len(prefix):]

        # Use textwrap to wrap the content of the line
        wrapper = textwrap.TextWrapper(
            width=width,
            initial_indent=prefix,
            subsequent_indent=prefix
        )
        reformatted_lines.extend(wrapper.wrap(content))

    return "\n".join(reformatted_lines)

def generate_comments(file_content, comment_format, comment_syntax, file_path):
    """
    Calls the Ollama CLI to generate comments for the given code.
    """
    prompt = f"""
    As an experienced software engineer, your task is to analyze the following code 
    and generate a comprehensive comment block that explains it.

    You have three strict rules:
    1. You MUST use the following comment syntax: {comment_syntax}
    2. The content of the comment block MUST strictly follow the format provided below. Replace @ai- with generate comments
    3. Each line in your response MUST NOT exceed 80 characters in length. Wrap all text 
       appropriately to adhere to this rule.

    --- CONTENT FORMAT START ---
    {comment_format}
    --- CONTENT FORMAT END ---

    Here is the code to analyze:
    --- CODE START ---
    {file_content}
    --- CODE END ---

    Generate ONLY the comment block, following all rules. Do not include 
    any other text, explanations, or the original code in your response.
    """

    try:
        command = ['ollama', 'run', OLLAMA_MODEL, prompt]
        print(f"   ▶️  Executing Ollama for {os.path.basename(file_path)}...")
        start_time = time.time()

        result = subprocess.run(
            command, capture_output=True, text=True, check=True,
            timeout=300, encoding='utf-8'
        )

        duration = time.time() - start_time
        print(f"   ✅ Ollama generation finished in {duration:.2f} seconds.")

        # MODIFIED: Use .rstrip() to preserve leading whitespace from the AI
        # while still cleaning the end of the output.
        return result.stdout.rstrip()

    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        print(f"   ❌ Error: Ollama command timed out after {duration:.0f} seconds.")
        return None
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return None


def process_file(file_path, comment_format, comment_syntax):
    """
    Reads a file, generates comments, and prepends them.
    """
    print(f"\n📄 Processing file: {file_path}")

    try:
        file_size_kb = os.path.getsize(file_path) / 1024
        print(f"   - File size: {file_size_kb:.2f} KB")

        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        if not original_content.strip():
            print("   ⚪ Skipping empty file.")
            return

        new_comments = generate_comments(original_content, comment_format, comment_syntax, file_path)

        if new_comments:
            # MODIFIED: Enforce 80-char limit programmatically
            print("   - Enforcing 80-character line limit...")
            new_comments = rewrap_comment_block(new_comments, width=80)

            new_content = f"{new_comments}\n\n{original_content}"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"   ✔️ Successfully added comments to {os.path.basename(file_path)}")
        else:
            print(f"   ⚠️ Failed to generate comments for {os.path.basename(file_path)}. Skipping.")

    except Exception as e:
        print(f"   ❌ An unexpected error occurred while processing {file_path}: {e}")


def main():
    """
    The main function to drive the script.
    """
    if len(sys.argv) != 2:
        print("Usage: python commenter.py <path_to_file_or_folder>")
        sys.exit(1)

    target_path = sys.argv[1]

    if not os.path.exists(target_path):
        print(f"Error: The path '{target_path}' does not exist.")
        sys.exit(1)

    try:
        with open('data/format.txt', 'r', encoding='utf-8') as f:
            comment_format = f.read()
        with open('data/syntax.txt', 'r', encoding='utf-8') as f:
            comment_syntax = f.read().strip()
    except FileNotFoundError as e:
        print(f"Error: Configuration file not found -> {e.filename}")
        print("Please ensure both 'format.txt' and 'syntax.txt' exist in the script's directory.")
        sys.exit(1)

    if os.path.isfile(target_path):
        process_file(target_path, comment_format, comment_syntax)
    elif os.path.isdir(target_path):
        print(f"📁 Processing all files in directory: {target_path}")
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.go', '.rs', '.java', '.dart')):
                    file_path = os.path.join(root, file)
                    process_file(file_path, comment_format, comment_syntax)

    print("\n✨ All done!")


if __name__ == "__main__":
    main()