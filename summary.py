import fnmatch
import typer
import json
from typing import List, Optional
from benchmark.config_read import read_dataset_config, read_engine_configs
from pathlib import Path
from functools import wraps

app = typer.Typer()

tested_datasets = [
	"random-100-euclidean", 
	"glove-25-angular",
	"random-match-keyword-100-angular-no-filters",
	"random-match-keyword-100-angular-filters", 
	"h-and-m-2048-angular-no-filters",
	"h-and-m-2048-angular-filters",
	"gist-960-euclidean",
	"laion-small-clip",
	"dbpedia-openai-1M-1536-angular"
]

search_pattern = r"-search-(\d+)-"
upload_pattern = r"-upload-"

def print_in_color(color="yellow"):
    # Define ANSI color codes
    colors = {
        "yellow": "\033[33m",         # Yellow
        "red": "\033[31m",            # Red
        "green": "\033[32m",          # Green
        "light blue": "\033[94m",     # Light Blue
        "orange": "\033[38;5;214m",   # Orange (approximation in ANSI)
        "reset": "\033[0m",           # Reset color
    }
    # Get the chosen color; default to yellow if the color is invalid
    chosen_color = colors.get(color.lower(), colors["yellow"])

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Set text color to chosen color
            print(chosen_color, end="")
            try:
                # Call the original function
                result = func(*args, **kwargs)
            finally:
                # Reset text color to default
                print(colors["reset"], end="")
            return result
        return wrapper
    return decorator

@print_in_color("light blue")
def show_upload_params(params : dict) -> None:
    print("Upload parameters:")
    print(f"parallel : {params.get('parallel', '')}")
    if params.get('engine') == 'milvus': print(f"index_params : {params.get('index_params', '')}")
    if params.get('engine') == 'qdrant':
        print(f"hnsw_config : {params.get('hnsw_config', '')}")
        print(f"optimizers_config : {params.get('optimizers_config', '')}")
    print()
    
def show_search_params(params : dict) -> None:
    print("Search parameters:")
    print(f"parallel : {params.get('parallel', '')}")
    print(f"config : {params.get('config', '')}")
    print()

@print_in_color("light blue")
def show_upload_results(results : dict) -> None:
    print("Upload results:")
    print(f"upload_time : {results.get('upload_time', '')}")
    print(f"total_time : {results.get('total_time', '')}")
    print()

def show_search_results(results : dict) -> None:
    print("Search results:")
    print(f"total_time : {results.get('total_time', '')}")
    print(f"mean_time : {results.get('mean_time', '')}")
    print(f"mean_precisions : {results.get('mean_precisions', '')}")
    print(f"std_time : {results.get('std_time', '')}")
    print(f"min_time : {results.get('min_time', '')}")
    print(f"max_time : {results.get('max_time', '')}")
    print(f"rps : {results.get('rps', '')}")
    print(f"p95_time : {results.get('p95_time', '')}")
    print(f"p99_time : {results.get('p99_time', '')}")
    print()

@app.command()
def summary(
    engines: List[str] = typer.Option(["*"], help="select qdrant, milvus engines (along with m, ef configurations)"),
    datasets: List[str] = typer.Option(["*"], help="select tested dataset(s)"),
    user_folder: str = typer.Option("Stefanos", help="choose the folder that contains the experiments", prompt="folder Nikos-Windows or Stefanos: "),
    upload: bool = typer.Option(False, help="Include upload operations", prompt="include upload? "),
    search: bool = typer.Option(False, help="Include search operations", prompt="include search? "),
    all_parallel: bool = typer.Option(False, help="Include all parallelism levels (1 and 100) (skip the below parameter)", prompt="include all parallelism levels - (and skip next prompt)? "),
    parallel: int = typer.Option(1, help="Specify the parallelism level (1 or 100)", prompt="parallelism for search: "),
    all_ef: bool = typer.Option(False, help="Include all ef levels (64, 128, 256, 512) (skip the below parameter)", prompt="include all ef levels - (and skip next prompt)? "),
    ef: int = typer.Option(128, help="config: ef for search operation (for HNSW algorithm) (64 - for qdrant only, for both DBs: 128, 256, 512)", prompt="ef for search: "),
    slow_show: bool = typer.Option(False, help="set if you want to see each experiment after pressing Enter")
):
    """
    Examples:
        python3 -m summary --engines "*-m-16-*" --datasets "glove-25-*"
        (minimum parameters)

        python3 -m summary --engines "*-m-16-*" --datasets "glove-25-*" --user-folder "Nikos-Windows" 
        (minimum parameters + user_folder)

        python3 -m summary --engines "*-m-16-*" --datasets "glove-25-*" --user-folder "Nikos-Windows" --upload --search --parallel 1 --ef 128
        (all parameters with specific parallel and ef values)

        python3 -m summary --engines "*-m-16-*" --datasets "glove-25-*" --user-folder "Nikos-Windows" --upload --search --all-parallel --all-ef
        (all parameters with all_parallel and all_ef flags)

        In promts, Enter is used to accept the default value. 
        Else, type the desired value and press Enter.
    """
    
    print()
    print(f"Selected engines: {engines}")
    print(f"Selected datasets: {datasets}")
    print(f"Selected folder: {user_folder}")
    print(f"Include upload: {upload}")
    print(f"Include search: {search}")
    print(f"Parallelism for search: All") if all_parallel else print(f"Parallelism for search: {parallel}")
    print(f"ef for search: All") if all_ef else print(f"ef for search: {ef}")
    
    all_engines = read_engine_configs()
    all_datasets = read_dataset_config()

    selected_engines = {
        name: config
        for name, config in all_engines.items()
        if any(fnmatch.fnmatch(name, engine) for engine in engines) and ("qdrant-m-" in name or "milvus-m-" in name)
    }

    selected_datasets = {
        name: config
        for name, config in all_datasets.items()
        if any(fnmatch.fnmatch(name, dataset) for dataset in datasets) and (name in tested_datasets)
    }

    # Experiments count
    count_experiments = 0
    print("\n*****\t Experiments count \t*****")
    for dataset_name, dataset_config in selected_datasets.items():
        for engine_name, engine_config in selected_engines.items():
            count_experiments += 1
            print(f"{count_experiments}. Engine: {engine_name} - Dataset: {dataset_name}")
    print(37*"*")
    print()
    # End of experiments count

    for dataset_name, dataset_config in selected_datasets.items():
        print(f"***** Dataset: {dataset_name} *****\n")
	
        for engine_name, engine_config in selected_engines.items():
            folder = Path(f"results/{user_folder}/{dataset_name}/{engine_name}")
            #print(f"Seeking inside {str(folder)} ...\n")
            print(f"\n{10*'*'}  Results of experiment: {engine_name} - {dataset_name}  {10*'*'}\n")
            
            for json_file in sorted(folder.rglob("*.json"), key=str):
                with open(json_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    #print(data)

                params = data.get("params", {})
                results = data.get("results", {})
                if upload and ("upload" in str(json_file)) : 
                    show_upload_params(params)
                    show_upload_results(results)
                if search and ("search" in str(json_file)) :
                    if ( all_parallel or params.get('parallel', 0) == parallel) and \
                        ( all_ef or params.get('config', {}).get('ef', 0) == ef or params.get('config', {}).get('hnsw_ef', 0) == ef) :
                        show_search_params(params)
                        show_search_results(results)
        if slow_show: input("Press Enter to proceed to next dataset: ")

if __name__ == "__main__":
    app()

