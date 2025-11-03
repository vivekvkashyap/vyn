import os
from typing import Any
import subprocess

def resolve_path(path: str) -> str:
    """Resolve a path to an absolute path, handling both relative and absolute paths."""
    if os.path.isabs(path):
        return path
    return os.path.abspath(os.path.join(os.getcwd(), path))

def call_tool(tool_name : str, tool_input : dict) -> Any:
    import json
    tool_input = json.loads(tool_input)
    print(f"Using tool: {tool_name}")
    if tool_name == "read_file":
        return read_file(tool_input["file_path"])
    elif tool_name == "edit_file":
        print("tool_input: ", tool_input)
        return edit_file(tool_input["file_path"], tool_input["new_content"])
    elif tool_name == "list_files":
        return list_files(tool_input["directory"])
    elif tool_name == "delete_file":
        return delete_file(tool_input["file_path"])
    elif tool_name == "search_file":
        return search_file(tool_input["file_path"])
    elif tool_name == "rename_file":
        return rename_file(tool_input["file_path"], tool_input["new_name"])
    elif tool_name == "move_file":
        return move_file(tool_input["file_path"], tool_input["new_path"])
    elif tool_name == "run_command":
        return run_command(tool_input["command"])
    elif tool_name == "list_directory_tree":
        return list_directory_tree(tool_input["directory"])
    elif tool_name == "read_file_content":
        return read_file_content(tool_input["file_path"])
    elif tool_name == "search_text_by_browser":
        return search_text_by_browser(tool_input["search_query"])
    elif tool_name == "grep_text":
        return grep_text(tool_input["directory"], tool_input["search_query"])
    elif tool_name == "index_codebase":
        return index_codebase(tool_input["file_path"])
    elif tool_name == "get_context_from_file":
        return get_context_from_file(tool_input["file_path"], tool_input["linerange"])
    elif tool_name == "make_directory":
        return make_directory(tool_input["directory_path"])
    else:
        raise ValueError(f"Tool {tool_name} not found")


def read_file(file_path : str) -> str:
    abs_path = resolve_path(file_path)
    with open(abs_path, 'r') as file:
        return "Reading the file: " + file.read()

def edit_file(file_path : str, new_content : str) -> str:
    abs_path = resolve_path(file_path)
    if not os.path.exists(abs_path):
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, 'w') as file:
        file.write(new_content)
    return "Editing the file: " + abs_path

def delete_file(file_path : str) -> str:
    abs_path = resolve_path(file_path)
    if not os.path.exists(abs_path):
        return "File not found: " + abs_path
    os.remove(abs_path)
    return "Deleting the file: " + abs_path

def search_file(file_path : str) -> str:
    abs_path = resolve_path(file_path)
    if not os.path.exists(abs_path):
        return "File not found: " + abs_path
    return "Searching the file: " + abs_path

def list_files(directory : str) -> str:
    abs_path = resolve_path(directory)
    if not os.path.exists(abs_path):
        return "Directory not found: " + abs_path
    files = os.listdir(abs_path)
    return "Listing the files in the directory: " + str(files)

def rename_file(file_path : str, new_name : str) -> str:
    abs_path = resolve_path(file_path)
    if not os.path.exists(abs_path):
        return "File not found: " + abs_path
    new_path = os.path.join(os.path.dirname(abs_path), new_name)
    os.rename(abs_path, new_path)
    return "Renaming the file: " + abs_path + " to " + new_path

def move_file(file_path : str, new_path : str) -> str:
    abs_path = resolve_path(file_path)
    target_path = resolve_path(new_path)
    if not os.path.exists(abs_path):
        return "File not found: " + abs_path
    os.rename(abs_path, target_path)
    return "Moving the file: " + abs_path + " to " + target_path

def run_command(command : str) -> str:
    try:
        return subprocess.run(command, shell=True, capture_output=True, text=True).stdout
    except Exception as e:
        return f"Error running command: {str(e)}"


def read_file_content(file_path : str) -> str:
    abs_path = resolve_path(file_path)
    if not os.path.exists(abs_path):
        return "File not found: " + abs_path
    with open(abs_path, 'r') as file:
        return file.read()

def list_directory_tree(directory : str) -> str:
    abs_path = resolve_path(directory)
    if not os.path.exists(abs_path):
        return "Directory not found: " + abs_path
    
    tree_lines = []
    tree_lines.append(f"Directory tree for: {abs_path}\n")
    
    for root, dirs, files in os.walk(abs_path):
        level = root.replace(abs_path, '').count(os.sep)
        indent = '  ' * level
        tree_lines.append(f"{indent}{os.path.join(root, os.path.basename(root))}/")
        
        sub_indent = '  ' * (level + 1)
        for file in files:
            tree_lines.append(f"{sub_indent}{file}")
    return '\n'.join(tree_lines)

def search_text_by_browser(text : str) -> str:
    """Search for text on the internet and return top 5 search results."""
    try:
        import requests
        from urllib.parse import quote
        from bs4 import BeautifulSoup
        
        search_url = f"https://html.duckduckgo.com/html/?q={quote(text)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            result_links = soup.find_all('a', class_='result__a', limit=5)
            
            for idx, link in enumerate(result_links, 1):
                title = link.get_text(strip=True)
                url = link.get('href', '')
                
                if title and url:
                    results.append(f"{idx}. {title}\n   URL: {url}")
            
            if results:
                return f"Top 5 search results for '{text}':\n\n" + "\n\n".join(results)
            else:
                return f"No search results found for '{text}'"
        else:
            return f"Error: Unable to perform search (Status code: {response.status_code})"
            
    except ImportError as e:
        missing_lib = str(e).split("'")[1] if "'" in str(e) else "required library"
        return f"Error: '{missing_lib}' library not installed. Install with: pip install {missing_lib}"
    except Exception as e:
        return f"Error searching for text: {str(e)}"


def grep_text(directory : str, search_query : str) -> str:
    """Search for text in files within a directory using grep."""
    abs_path = resolve_path(directory)
    if not os.path.exists(abs_path):
        return "Directory not found: " + abs_path
    
    try:
        import subprocess
        
        result = subprocess.run(
            ['grep', '-r', '-n', search_query, abs_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                return f"Found matches for '{search_query}':\n\n{output}"
            else:
                return f"Text not found in the directory: {abs_path}"
        elif result.returncode == 1:
            return f"Text not found in the directory: {abs_path}"
        else:
            return f"Error running grep: {result.stderr}"
            
    except FileNotFoundError:
        return "Error: 'grep' command not found. This function requires grep to be installed."
    except subprocess.TimeoutExpired:
        return "Error: Search timed out (took longer than 30 seconds)"
    except Exception as e:
        return f"Error searching for text: {str(e)}"


def make_directory(directory_path: str) -> str:
    """Make a directory."""
    try:
        abs_path = resolve_path(directory_path)
        os.makedirs(abs_path, exist_ok=True)
        return "Directory created: " + abs_path
    except Exception as e:
        return f"Error creating directory: {str(e)}"

def get_context_from_file(file_path: str, linerange: list[int]) -> str:
    """Get the context of a codebase file for a given line range."""
    abs_path = resolve_path(file_path)
    if not os.path.exists(abs_path):
        return "File not found: " + abs_path
    with open(abs_path, 'r') as file:
        content = file.read()
    lines = content.split('\n')
    return '\n'.join(lines[linerange[0]-1:linerange[1]])



def index_codebase(file_path: str) -> str:
    """Index a codebase file by creating an embedding vector using OpenAI's text-embedding-3-small model."""
    try:
        from openai import OpenAI
        import json
        
        abs_path = resolve_path(file_path)
        if not os.path.exists(abs_path):
            return "File not found: " + abs_path
        
        with open(abs_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "Error: OPENAI_API_KEY environment variable is not set"
        
        client = OpenAI(api_key=api_key)
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=content
        )
        
        embedding_vector = response.data[0].embedding
        
        embeddings_dir = os.path.join(os.path.dirname(abs_path), "embeddings")
        os.makedirs(embeddings_dir, exist_ok=True)
        
        base_filename = os.path.basename(abs_path)
        embedding_file_path = os.path.join(embeddings_dir, base_filename + ".embedding.json")
        
        embedding_data = {
            "file_path": abs_path,
            "model": "text-embedding-3-small",
            "embedding": embedding_vector,
            "content_length": len(content)
        }
        
        with open(embedding_file_path, 'w', encoding='utf-8') as f:
            json.dump(embedding_data, f)
        
        return f"Successfully indexed file: {abs_path}\nEmbedding stored at: {embedding_file_path}\nEmbedding dimension: {len(embedding_vector)}"
        
    except ImportError as e:
        missing_lib = str(e).split("'")[1] if "'" in str(e) else "required library"
        return f"Error: '{missing_lib}' library not installed. Install with: pip install {missing_lib}"
    except Exception as e:
        return f"Error indexing codebase: {str(e)}"