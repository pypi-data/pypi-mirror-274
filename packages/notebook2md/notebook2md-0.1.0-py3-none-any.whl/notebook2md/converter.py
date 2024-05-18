import nbformat
from nbconvert import MarkdownExporter
import sys
import os

def convert_ipynb_to_md(ipynb_file, output_dir=None):
    # Check if the input file exists
    if not os.path.isfile(ipynb_file):
        print(f"Error: The file {ipynb_file} does not exist.")
        return

    # Load the Jupyter notebook
    with open(ipynb_file, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    # Create an instance of the MarkdownExporter
    markdown_exporter = MarkdownExporter()
    
    # Convert the notebook to Markdown
    markdown_data, resources = markdown_exporter.from_notebook_node(notebook)
    
    # Determine output path
    base_name = os.path.splitext(os.path.basename(ipynb_file))[0]
    if output_dir:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = os.path.join(output_dir, f"{base_name}.md")
    else:
        output_file = f"{base_name}.md"
    
    # Write the converted Markdown to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_data)
    
    print(f"Conversion complete: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m notebook2md <path_to_ipynb_file> [<output_directory>]")
    else:
        ipynb_file = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        convert_ipynb_to_md(ipynb_file, output_dir)