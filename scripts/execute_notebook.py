"""Execute the notebook using nbclient directly under Python 3.14."""
import nbformat
from nbclient import NotebookClient
import os

notebook_path = os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'retail_sales_eda.ipynb')
notebook_path = os.path.abspath(notebook_path)
output_path = notebook_path  # overwrite in-place with executed version

print(f"Loading notebook: {notebook_path}")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Use the python314 kernel we registered
nb.metadata.kernelspec = {
    "display_name": "Python 3.14",
    "language": "python",
    "name": "python314"
}

client = NotebookClient(
    nb,
    timeout=600,
    kernel_name='python314',
    resources={'metadata': {'path': os.path.dirname(notebook_path)}}
)

print("Executing notebook cells...")
try:
    client.execute()
    print("All cells executed successfully!")
except Exception as e:
    print(f"Error during execution: {e}")
    raise
finally:
    # Save even if there was an error (partial execution)
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"Notebook saved to: {output_path}")
