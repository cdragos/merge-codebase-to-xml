# Code File Merger to XML

This tool merges specified code files into a structured XML format, with support for scanning directories and selecting individual files. The generated XML can also be used as context for O(1) type models.

## Features

- Merge multiple code files into a single XML document
- Support for various code file extensions (`.py`, `.ts`, `.jsx`, `.js`, `.tsx`)
- Scan a directory recursively for files or specify individual files
- Pretty-printed XML output

## Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Ensure Python 3.x is installed on your system.

## Usage

To run the tool, you can either scan a directory for code files or specify individual files directly.

### Command-line Arguments:

- `--input-dir`: The path to a directory containing code files to include in the XML.
- `--file`: Path to individual files (can be used multiple times).
- `--output-file`: The path to save the generated XML file (required).

### Example Commands:

1. **Scan a Directory for Files:**

    ```bash
    python merge_code_to_xml.py --input-dir ./path/to/code --output-file ./output/codebase.xml
    ```

2. **Specify Individual Files:**

    ```bash
    python merge_code_to_xml.py --file ./path/to/file1.py --file ./path/to/file2.js --output-file ./output/codebase.xml
    ```

3. **Mixing Directory and Files:**

    ```bash
    python merge_code_to_xml.py --input-dir ./path/to/code --file ./path/to/specific_file.ts --output-file ./output/codebase.xml
    ```

### Output

The tool will generate an XML file at the specified output location with the following structure:

```xml
<codebase>
    <file>
        <filename>file1.py</filename>
        <filepath>/absolute/path/to/file1.py</filepath.json<|meta_end|></filepath>
        <contents>... file contents ...</contents>
    </file>
    <!-- More files -->
</codebase>
