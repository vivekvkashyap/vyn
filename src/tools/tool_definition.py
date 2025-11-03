

tool_definitions = [
    # edit_file tool
    {
        "type": "function",
        "name": "edit_file",
        "description": "Edits the contents of the given file. If the file does not exist, it will be created.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to edit. Can be a relative path (resolved from current working directory) or absolute path."
                },
                "new_content": {
                    "type": "string",
                    "description": "New content to write to the file."
                }
            },
            "required": ["file_path", "new_content"],
            "additionalProperties": False
        }
    },
    # list_files tool
    {
        "type": "function",
        "name": "list_files",
        "description": "Lists the files in the given directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Path to the directory to list files from. Can be a relative path (resolved from current working directory) or absolute path."
                }
            },
            "required": ["directory"],
            "additionalProperties": False
        }
    },
    # read_file tool
    {
        "type": "function",
        "name": "read_file",
        "description": "Reads the contents of the given file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read."
                }
            },
            "required": ["file_path"],
            "additionalProperties": False
        }
    },

    # delete_file tool
    {
        "type": "function",
        "name": "delete_file",
        "description": "Deletes the given file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to delete."
                }
            },
            "required": ["file_path"],
            "additionalProperties": False
        }
    },
    # search_file tool
    {
        "type": "function",
        "name": "search_file",
        "description": "Searches the given file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to search."
                }
            },
            "required": ["file_path"],
            "additionalProperties": False
        }
    },
    # rename_file tool
    {
        "type": "function",
        "name": "rename_file",
        "description": "Renames the given file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",   
                    "description": "Path to the file to rename."
                },
                "new_name": {
                    "type": "string",
                    "description": "New name for the file."
                }
            },
            "required": ["file_path", "new_name"],
            "additionalProperties": False
        }
    },
    # move_file tool
    {
        "type": "function",
        "name": "move_file",
        "description": "Moves the given file to the new path.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to move. Can be a relative path (resolved from current working directory) or absolute path."
                },
                "new_path": {
                    "type": "string",
                    "description": "New path to move the file to. Can be a relative path (resolved from current working directory) or absolute path."
                }
            },
            "required": ["file_path", "new_path"],
            "additionalProperties": False
        }
    },

    # run_command tool
    {
        "type": "function",
        "name": "run_command",
        "description": "Runs the given command.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Command to run."
                },
            },
            "required": ["command"],
            "additionalProperties": True
        }
    },
    # list_directory_tree tool
    {
        "type": "function",
        "name": "list_directory_tree",
        "description": "Lists the directory tree of the given directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Path to the directory to list the tree of."
                }
            },
            "required": ["directory"],
            "additionalProperties": False
        }
    },
    # read_file_content tool
    {
        "type": "function",
        "name": "read_file_content",
        "description": "Reads the contents of the given file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read the content of."
                }
            },
            "required": ["file_path"],
            "additionalProperties": False
        }
    },
    # search_text_by_browser tool
    {
        "type": "function",
        "name": "search_text_by_browser",
        "description": "Searches the given text on the internet.",
        "parameters": {
            "type": "object",
            "properties": {
                "search_query": {
                    "type": "string",
                    "description": "Text to search for on the internet."
                }
            },
            "required": ["search_query"],
            "additionalProperties": False
        }
    },
    # grep_text tool
    {
        "type": "function",
        "name": "grep_text",
        "description": "Searches the given text in the given directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Path to the directory to search the text in."
                },
                "search_query": {
                    "type": "string",
                    "description": "Text to search for in the directory."
                }
            },
            "required": ["directory", "search_query"],
            "additionalProperties": False
        }
    },
    # index_codebase tool
    {
        "type": "function",
        "name": "index_codebase",
        "description": "Indexes the given codebase file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the codebase file to index."
                }
            },
            "required": ["file_path"],
            "additionalProperties": False
        }
    },
    # get_context_from_file tool
    {
        "type": "function",
        "name": "get_context_from_file",
        "description": "Gets the context of the given codebase file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the codebase file to get the context from."
                },
                "linerange": {
                    "type": "array",
                    "description": "Line range to get the context from.",
                    "items": {
                        "type": "integer"
                    },
                    "minItems": 2,
                    "maxItems": 2
                }
            },
            "required": ["file_path", "linerange"],
            "additionalProperties": False
        }
    },
    # make_directory tool
    {
        "type": "function",
        "name": "make_directory",
        "description": "Makes a directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory_path": {
                    "type": "string",
                    "description": "Path to the directory to make."
                }
            },
            "required": ["directory_path"],
            "additionalProperties": False
        }
    }
]