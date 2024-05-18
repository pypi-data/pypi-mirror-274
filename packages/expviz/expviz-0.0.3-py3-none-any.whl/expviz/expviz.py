import pandas as pd
from tabulate import tabulate
from IPython.display import display, HTML
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import copy 

# Set global display options
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

def format_with_specified_pattern(number, pattern):
    formatted_number = pattern.format(number)
    
    # 分离整数和小数部分
    if '.' in formatted_number:
        integer_part, fractional_part = formatted_number.split('.')
    else:
        integer_part, fractional_part = formatted_number, ''
    
    # 计算总有效数字个数
    significant_digits = len(integer_part.replace('-', '')) + len(fractional_part)
    
    # 补齐零
    if significant_digits < 3:
        if '.' not in formatted_number:
            formatted_number += '.'
        formatted_number += '0' * (3 - significant_digits)
    
    return formatted_number

# Function to convert nested dictionary to DataFrame
def dict_to_dataframe(data, fmt='{:,.3g}', transpose = False, bold_col_max = False, bold_col_max_exclude_rows = [], cell_transform = lambda x : x):
    data = copy.deepcopy(data)
    for exp in data:
        for metric in data[exp]:
            try:
                data[exp][metric] = format_with_specified_pattern(cell_transform(data[exp][metric]), fmt) if type(data[exp][metric]) is float else data[exp][metric]
            except:
                pass
    df = pd.DataFrame(data).T
    if transpose:
        df = df.T
    if bold_col_max:
        # Define the rows to be excluded from the max calculation
        exclude_rows = bold_col_max_exclude_rows

        # Function to apply LaTeX bold formatting to the max value in a Series excluding specified rows
        def apply_latex_bold_exclude(s):
            # Convert to numeric and ignore errors; non-numeric become NaN
            numeric_s = pd.to_numeric(s, errors='coerce')
    
            # Exclude specified rows from max calculation
            max_val = numeric_s.drop(index=exclude_rows).max()
            
            # Apply LaTeX bold formatting to the max value if it's not in the excluded rows and is a number
            # Keep the original string if it's NaN or non-numeric
            return [f"\\textbf{{{val}}}" if idx not in exclude_rows and pd.notnull(numeric_s[idx]) and val == max_val else s[idx] for idx, val in enumerate(numeric_s)]
        df = df.apply(apply_latex_bold_exclude)
    return df

# Function to convert DataFrame to LaTeX
def to_latex(data, fmt='{:,.3g}', transpose=False, escape=None, **kwargs):
    df = dict_to_dataframe(data, fmt = fmt, transpose = transpose, **kwargs)
    latex_code = df.to_latex(escape=escape)
    
    # Fit the LaTeX table into the template
    table_tmp = """\\begin{table}[t]
    \\centering
    \\scriptsize
    
    %s
    \caption{Caption Title.}
    \label{tab:tablename}
\end{table}
    """
    return table_tmp % latex_code.replace("\n", "\n    ")

# Function to convert DataFrame to Markdown
def to_markdown(data, fmt='{:,.3g}', transpose=False):
    df = dict_to_dataframe(data, fmt = fmt, transpose = transpose)
    markdown_table = tabulate(df, tablefmt="pipe", headers="keys")
    return markdown_table

# Function to display DataFrame in Jupyter
def show(data, fmt='{:,.3g}', transpose=False, **kwargs):
    df = dict_to_dataframe(data, fmt = fmt, transpose = transpose, **kwargs)
    display(HTML(df.to_html()))

def read_results(baseurl, expnames, filename="eval.json", score_metrics=None):
    results = {}
    
    def load_and_filter(filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                data = json.load(file)
                # Filter the scores if score_metrics is provided
                if score_metrics is not None:
                    data = {k: v for k, v in data.items() if k in score_metrics}
                return data
        else:
            print(f"File not found: {filepath}")
            return None
    
    if isinstance(expnames, list):
        for expname in expnames:
            filepath = os.path.join(baseurl, expname, filename)
            data = load_and_filter(filepath)
            if data is not None:
                results[expname] = data
    elif isinstance(expnames, dict):
        for key, value in expnames.items():
            filepath = os.path.join(baseurl, value, filename)
            data = load_and_filter(filepath)
            if data is not None:
                results[key] = data
    else:
        print("Invalid expnames type. It should be either a list or a dict.")
    
    return results

def plot_data(data, colormap='Set3', fontsize=22, figsize=(10, 6), save_path=None, xlabel=None, ylabel=None, xscale=None, yscale=None):
    """
    Plots the given data with configurable parameters.
    
    :param data: Dictionary containing the data to be plotted.
                The format of the data should be:
                {
                    'task1': {
                        'x1': {'score_name1': score_value1},
                        'x2': {'score_name1': score_value2},
                        ...
                    },
                    'task2': {
                        'x2': {'score_name2': score_value1},
                        'x2': {'score_name2': score_value2},
                        ...
                    },
                    ...
                }
    :param colormap: String, the colormap to be used. Default is 'Set3'.
    :param fontsize: Integer, the font size to be used. Default is 22.
    :param figsize: Tuple, the figure size. Default is (10, 6).
    :param save_path: String, path to save the plot. If None, the plot is not saved. Default is None.
    :param xlabel: String, label for the x-axis. If None, it is left blank. Default is None.
    :param ylabel: String, label for the y-axis. If None, the score name is used. Default is None.
    :param xscale: String, scale for the x-axis. If None, no scaling is applied. Default is None.
    :param yscale: String, scale for the y-axis. If None, no scaling is applied. Default is None.
    """
    # Get color map
    cmap = plt.get_cmap(colormap)
    
    # Define a variety of different markers
    markers = ['o', 's', '*', 'D', '^', 'v', '<', '>', 'p', 'H', '+', 'x', '|', '_']
    
    # Define different line styles
    line_styles = ['-', '--', '-.', ':']
    
    # Set plot parameters
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams["figure.figsize"] = figsize

    first_key = next(iter(data))
    if isinstance(data[first_key], list):
        for idx, (task, task_data) in enumerate(data.items()):
            xs, ys = task_data
            plt.plot(xs, ys, label=task, marker=markers[idx % len(markers)], linestyle=line_styles[idx % len(line_styles)], color=cmap.colors[idx], markerfacecolor='white', linewidth=2.0)
    else:
        for idx, (task, task_data) in enumerate(data.items()):
            sorted_keys = sorted(task_data.keys(), key=float)
            xs = [float(key) for key in sorted_keys]
            ys = [list(val.values())[0] for key in sorted_keys for val in [task_data[key]]]
            if ylabel is None:
                ylabel = list(task_data[sorted_keys[0]].keys())[0]
            plt.plot(xs, ys, label=task, marker=markers[idx % len(markers)], linestyle=line_styles[idx % len(line_styles)], color=cmap.colors[idx], markerfacecolor='white', linewidth=2.0)
    
    # Set scales if provided
    if xscale:
        plt.xscale(xscale)
    if yscale:
        plt.yscale(yscale)
    
    plt.xlabel(xlabel if xlabel else '')
    plt.ylabel(ylabel)
    plt.legend(labelspacing=0)
    plt.grid(True, linestyle='--')
    
    # Save and show the plot
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()
