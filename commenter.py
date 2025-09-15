import sys
import os
import subprocess
import time

# --- Configuration ---
# You can change this to a smaller model like "phi3:mini" for better speed
OLLAMA_MODEL = "phi3"

# --- Main Script Logic ---

def generate_comments(file_content, comment_format, file_path):
    """
    Calls the Ollama CLI to generate comments for the given code.
    (Implements Step 2)
    """
    prompt = f"""
    As an experienced software engineer, your task is to analyze the following code 
    and generate a comprehensive comment block that explains it.

    The comment block MUST strictly follow this format:
    --- FORMAT START ---
    {comment_format}
    --- FORMAT END ---

    Here is the code to analyze:
    --- CODE START ---
    {file_content}
    --- CODE END ---

    Generate ONLY the comment block based on the provided format. Do not include 
    any other text, explanations, or the original code in your response.
    """

    try:
        command = ['ollama', 'run', OLLAMA_MODEL, prompt]
        print(f"   ▶️  Executing Ollama for {os.path.basename(file_path)}...")
        start_time = time.time()

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=300,  # Increased timeout to 5 minutes
            encoding='utf-8'
        )

        duration = time.time() - start_time
        print(f"   ✅ Ollama generation finished in {duration:.2f} seconds.")
        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        print(f"   ❌ Error: Ollama command timed out after {duration:.0f} seconds.")
        return None
    except FileNotFoundError:
        print("❌ Error: 'ollama' command not found. Please ensure it's in your system's PATH.")
        return None
    except subprocess.CalledProcessError as e:
        stderr_output = e.stderr.strip() if e.stderr else "No stderr output captured."
        print(f"❌ Error executing Ollama CLI. Stderr: {stderr_output}")
        return None
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return None


def process_file(file_path, comment_format):
    """
    Reads a file, generates comments, and prepends them.
    (Implements Steps 1 and 3)
    """
    print(f"\n📄 Processing file: {file_path}")

    try:
        file_size_kb = os.path.getsize(file_path) / 1024
        print(f"   - File size: {file_size_kb:.2f} KB")

        # Step 1: Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        if not original_content.strip():
            print("   ⚪ Skipping empty file.")
            return

        # Step 2 (delegated): Get the comments from the AI
        new_comments = generate_comments(original_content, comment_format, file_path)

        # Step 3: Prepend comments and write back to the file
        if new_comments:
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
    (Implements Step 4)
    """
    if len(sys.argv) != 2:
        print("Usage: python commenter.py <path_to_file_or_folder>")
        sys.exit(1)

    target_path = sys.argv[1]

    if not os.path.exists(target_path):
        print(f"Error: The path '{target_path}' does not exist.")
        sys.exit(1)

    try:
        with open('format.txt', 'r', encoding='utf-8') as f:
            comment_format = f.read()
    except FileNotFoundError:
        print("Error: `format.txt` not found in the script's directory.")
        sys.exit(1)

    if os.path.isfile(target_path):
        process_file(target_path, comment_format)
    # Step 4: Loop if the path is a directory
    elif os.path.isdir(target_path):
        print(f"📁 Processing all files in directory: {target_path}")
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.go', '.rs', '.java', '.dart')):
                    file_path = os.path.join(root, file)
                    process_file(file_path, comment_format)

    print("\n✨ All done!")


if __name__ == "__main__":
    main()