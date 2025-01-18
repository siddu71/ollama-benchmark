import argparse
import yaml
import subprocess
import ollama

parser = argparse.ArgumentParser(
    prog="python3 check_models.py",
    description="Before running check_models.py, please make sure you installed ollama successfully \
        on macOS, Linux, or WSL2 on Windows. You can check the website: https://ollama.ai",
    epilog="Author: Jason Chuang")

parser.add_argument("-v",
                    "--verbose",
                    action="store_true",
                    help="this program helps you check whether you have ollama benchmark models installed")

parser.add_argument("-m",
                    "--models",
                    type=str,
                    help="provide benchmark models YAML file path. ex. ../data/benchmark_models.yml")


def parse_yaml(yaml_file_path):
    with open(yaml_file_path, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
            data = {}
    return data


def get_local_models():
    """Fetch the list of locally available models."""
    result = subprocess.run(['ollama', 'list'], stdout=subprocess.PIPE, text=True)
    local_models = []
    if result.returncode == 0:
        for line in result.stdout.splitlines()[1:]:  # Skip the header line
            parts = line.split()
            if len(parts) > 0:
                local_models.append(parts[0])  # Model name is the first column
    return local_models


def pull_models(models_file_path):
    print(f"LLM models file path: {models_file_path}")
    print("Checking and pulling the following LLM models")
    models_dict = parse_yaml(models_file_path)
    local_models = get_local_models()
    for x in models_dict['models']:
        model_name = x['model']
        if model_name in local_models:
            print(f"Model '{model_name}' already exists locally. Skipping pull.")
        else:
            print(f"Pulling model '{model_name}'...")
            try:
                ollama.pull(model_name)
            except Exception as e:
                print(f"Failed to pull model '{model_name}': {e}")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.models is not None:
        print(f"args.models file path: {args.models}")
        pull_models(args.models)
    else:
        print("No models file provided. Use -m to specify the path to a benchmark models YAML file.")

