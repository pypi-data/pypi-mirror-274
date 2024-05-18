# notebook2md

`notebook2md` is a Python package that allows you to convert Jupyter notebooks to Markdown files.

## Installation

You can install `notebook2md` using pip:

```sh
pip install notebook2md
```

## Usage

To convert a Jupyter notebook to a Markdown file, use the `notebook2md` command followed by the path to the .ipynb file and optionally, the output directory:

```sh
notebook2md <path_to_ipynb_file> [<output_directory>]
```

## Project Structure

The `notebook2md` package includes the following files:

- `notebook2md/__init__.py`: Initialization file for the `notebook2md` package.
- `notebook2md/converter.py`: Contains the code for the `notebook2md` module. It exports a function `convert_ipynb_to_md` that converts Jupyter notebooks to Markdown files.
- `tests/__init__.py`: Initialization file for the `tests` package.
- `tests/test_converter.py`: Contains the unit tests for the `notebook2md` module. It includes a test case `TestConverter` with a method `test_conversion` to test the `convert_ipynb_to_md` function.
- `README.md`: Documentation for the project.
- `setup.py`: Setup script for the package. It includes the package metadata, dependencies, and entry points.
- `LICENSE`: License information for the project.
- `requirements.txt`: Lists the dependencies required for the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, you can reach out to the author at shpetim@gmail.com.

## Project Link

You can find the project on GitHub at [https://github.com/shpetimhaxhiu/notebook2md](https://github.com/shpetimhaxhiu/notebook2md).