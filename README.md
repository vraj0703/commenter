
---

# **AI Code Commenter**

An intelligent command-line tool that uses local Ollama models to automatically generate high-quality, structured comments for your code.

The **AI Code Commenter** is designed for developers who value security, customization, and efficiency. By leveraging the power of local Large Language Models (LLMs), it offers several key advantages:

* 🔒 **Code Security & Privacy**: Your code is never sent to a third-party API. All processing happens entirely on your local machine, ensuring your intellectual property remains private and secure.
* ⚙️ **Exhaustive Customization**: The tool is not hardcoded for any specific language or style. Through simple text files (format.txt for content and syntax.txt for style), you can adapt it to any programming language, codebase, or team's coding standards.
* 🚀 **Workflow Automation**: Quickly document a single file or an entire project with a single command, saving you time and improving the maintainability of your code.

---

## **Features**

* **Local First**: Operates entirely offline using your own Ollama instance.
* **Highly Configurable**: Define comment content and syntax using simple text files.
* **CLI-Based**: Easy to integrate into scripts and automated workflows.
* **Batch Processing**: Run on a single file or recursively through an entire folder.
* **Intelligent Setup**: Automatically checks for Ollama, manages models, and sets up user-friendly configuration files on the first run.

---

## **Installation & Setup**

Follow these steps to get the commenter tool up and running.

### **Step 1: Install Ollama**

The commenter tool requires Ollama to be running on your system.

* **Linux & macOS**: Run the following command in your terminal.
  > ```curl \-fsSL https://ollama.com/install.sh | sh```

* **Windows**: Download and run the installer from the [Ollama website](https://ollama.com/).

After installing, you need to pull a model. llama3 is a great choice for quality. For faster performance on less powerful hardware, phi3:mini is an excellent alternative.

Pull a high-quality model (recommended)  
>```ollama pull llama3```

\# Or pull a smaller, faster model  
>```ollama pull phi3:mini```

**Important**: Make sure the Ollama application is running before you use the commenter tool.

### **Step 2: Install the Commenter Tool**

Install the tool directly from PyPI using pip.

>```pip install ai-code-commenter-vraj0703```

### **Step 3: First-Time Configuration**

The first time you run the config command, the tool will automatically create a configuration directory and default templates on your system.

>```commenter config```

This command will:

1. Verify that Ollama is installed.
2. Create a folder at ```\~/.config/commenter/``` (this path works for Linux, macOS, and Windows).
3. Copy default ```format.txt``` and ```syntax.txt``` files into it, which you can then customize.

---

## **Configuration**

You can easily configure the tool to fit your needs using the config command.

### **Setting the Ollama Model**

You can tell the commenter which Ollama model to use. If the model isn't downloaded, the tool will pull it for you.

>```commenter config \--model phi3:mini```

### **Customizing Comment Templates**

The real power of this tool comes from its configurable templates. The config command allows you to point the tool to your own custom template files.

Example for a project using custom Java templates 

>```commenter config \--format-path "/path/to/my/java\_format.txt" \--syntax-path "/path/to/my/java\_syntax.txt"```

If you don't set custom paths, the tool will use the default files located in \~/.config/commenter/.

#### format.txt \- The Content and Structure

This file controls **what** goes inside your comments. You can define placeholders for the AI to fill in.

*Example format.txt:*

> Author: AI Assistant  
> Date: \<CURRENT\_DATE\>  
> Description: <A high-level summary of the file's purpose.\>
> 
> Functions:\- \<function\_name\_1\>: \<Brief description of what this function does.\>

#### **syntax.txt \- The Comment Style**

This file tells the AI **how** to write the comment for a specific language.

*Example syntax.txt for Java/JavaScript:*

>The entire comment block must be a valid documentation comment. It must start with \`/\*\*\` on its own line, each line must begin with a \` \* \`, and it must end with \` \*/\` on its own line.

*Example syntax.txt for Python:*

>Every single line of the comment block must start with a \`\#\` character followed by a space.

---

## **Usage**

Once configured, using the tool is simple. Use the run command followed by the path to your code.

### **Commenting a Single File**

> ```commenter run /path/to/your/file.py```

### **Commenting an Entire Folder**

The tool will find and comment on all supported source files within the folder and its subdirectories.

>```commenter run /path/to/your/project/```

---

## **Troubleshooting**

* **"Ollama is not installed" Error**:
    * Ensure the Ollama desktop application is running.
    * Make sure you have run the Ollama installation script, and the ollama command is available in your system's PATH.
* **Timeout Errors**:
    * The first time you use a model, Ollama needs to load it into memory, which can be slow. Try "warming up" the model by running ```ollama run \<your\_model\_name\> "Hello\!"``` in your terminal first.
    * Consider using a smaller model (phi3:mini) for faster processing by running ```commenter config \--model phi3:mini```.
* **Resetting Configuration**:
    * If your configuration files get corrupted, you can safely delete the ```\~/.config/commenter``` directory. The next time you run commenter config, the folder and default files will be recreated.

---

## **Contributing & Support**

This project is open source. If you find a bug or have a feature request, please open an issue on our GitHub repository.

* **GitHub Repository**: [vraj0703/commenter](https://github.com/vraj0703/commenter)