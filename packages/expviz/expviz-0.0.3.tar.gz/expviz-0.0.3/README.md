# Experiments Visualization Toolkit (ExpViz)

Welcome to the Experiments Visualization Toolkit (ExpViz), a Python-based solution designed to facilitate the handling and visualization of experiment results, particularly those stored in JSON format. Whether your results are stored in files or represented as JSON-like dictionaries, ExpViz is here to streamline your data visualization process.

[![GitHub Repo](https://img.shields.io/badge/github-repo-green.svg?style=flat&logo=github)](https://github.com/fuzihaofzh/expviz)

## Features

- **Read Results**: Directly input JSON-like dictionaries or read experiment results from JSON files in a specified directory.
- **Convert to DataFrame**: Elegantly transform nested dictionaries into customizable Pandas DataFrames.
- **Table Rendering**: Convert DataFrames to LaTeX and Markdown tables for seamless integration into documents and web pages.
- **Jupyter Display**: Render and showcase DataFrames interactively within Jupyter notebooks.

## Installation

```sh
# Clone the repository
git clone https://github.com/fuzihaofzh/expviz.git

# Navigate to the cloned repository
cd expviz

# (Optional) Install any dependencies listed in requirements.txt
pip install -r requirements.txt
```

## Usage

### 1. Reading Results

```python
# Directly using a JSON-like dictionary
data_dict = {
    "exp1": {"Score1": 10.1, "Score2": 20},
    "exp2": {"Score1": 30, "Score2": None}
}
results = read_results(data_dict=data_dict)

# Alternatively, using the base URL and experiment names
baseurl = "path/to/experiment/results"
expnames = ["experiment1", "experiment2"]  # or {"exp1": "experiment1", "exp2": "experiment2"}
results = read_results(baseurl, expnames, filename="eval.json")
```

### 2. Converting to DataFrame

```python
# Format and convert the results to a DataFrame
df = dict_to_dataframe(results, fmt='{:,.3g}', transpose=False)
print(df)
```

### 3. Rendering as LaTeX or Markdown

```python
# Convert the DataFrame to a LaTeX table
latex_table = to_latex(results, fmt='{:,.3g}', transpose=False)
print(latex_table)

# Convert the DataFrame to a Markdown table
markdown_table = to_markdown(results, fmt='{:,.3g}', transpose=False)
print(markdown_table)
```

### 4. Displaying in Jupyter

```python
# Visualize the DataFrame in a Jupyter notebook
show(results, fmt='{:,.3g}', transpose=False)
```

## Examples

- **Using JSON-like Dictionary**

    ```python
    data_dict = {
        "exp1": {"Score1": 10.1, "Score2": 20},
        "exp2": {"Score1": 30, "Score2": None}
    }
    results = read_results(data_dict=data_dict)
    ```

- **Using a List of Experiments**

    ```python
    results = read_results("path/to/results", ["experiment1", "experiment2"])
    ```

- **Using a Dictionary of Experiments**

    ```python
    results = read_results("path/to/results", {"exp1": "experiment1", "exp2": "experiment2"})
    ```

- **Visualizing in Jupyter Notebook**

    ```python
    show(results)
    ```

- **Rendering as Markdown**

    ```python
    md_table = to_markdown(results)
    print(md_table)
    ```

## Contributing

Contributions are warmly welcomed! For information on how to contribute, please refer to our [contributing guidelines](CONTRIBUTING.md).

## License

ExpViz is under the MIT License. For more details, check out the [LICENSE.md](LICENSE.md) file in our GitHub repository.