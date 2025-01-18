import argparse
import tabulate
import yaml
import subprocess
import datetime
import time
from tabulate import tabulate

parser = argparse.ArgumentParser(
    prog="python3 check_models.py",
    description="Benchmark LLM models using ollama, focusing on chat chaining and realistic tokens/s.",
    epilog="Author: Jason Chuang"
)

parser.add_argument("-v", "--verbose",
                    action="store_true",
                    help="Print more details during execution")

parser.add_argument("-m", "--models",
                    type=str,
                    help="Path to a benchmark models YAML file, e.g., ../data/benchmark_models.yml")

parser.add_argument("-b", "--benchmark",
                    type=str,
                    help="Path to a benchmark config YAML, e.g., ../data/benchmark1.yml")

parser.add_argument("-t", "--type",
                    type=str,
                    help="Type of benchmark scenario (e.g., chat, instruct, etc.)")

def parse_yaml(yaml_file_path):
    """ Safely parse a YAML file. """
    try:
        with open(yaml_file_path, 'r') as stream:
            return yaml.safe_load(stream)
    except FileNotFoundError:
        print(f"Error: File not found - {yaml_file_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return {}

def approximate_token_count(text):
    """ Approximate token count using a simple word-to-token ratio. """
    words = text.strip().split()
    return int(len(words) * 0.75)

def run_benchmark(models_file_path, benchmark_file_path, scenario_type, ollamabin):
    models_dict = parse_yaml(models_file_path)
    benchmark_dict = parse_yaml(benchmark_file_path)

    allowed_models = {m['model'] for m in models_dict.get('models', [])}
    results = {}
    table_data = []

    for block in benchmark_dict.get('modeltypes', []):
        if block.get('type') == scenario_type:
            print("Scenario Type:", scenario_type)
            prompts = block.get('prompts', [])
            model_list = block.get('models', [])

            for model_info in model_list:
                model_name = model_info.get('model')
                if model_name not in allowed_models:
                    continue

                loc_dt = datetime.datetime.now()
                log_filename = f"log_{loc_dt.strftime('%Y-%m-%d-%H%M%S')}.log"
                print(f"Model Name = {model_name}")
                stored_tps = []
                conversation_text = ""

                with open(log_filename, "w", encoding='utf-8') as logf:
                    logf.write(f"Model Name = {model_name}\n")

                    for prompt_item in prompts:
                        user_prompt = prompt_item.get('prompt', '').strip()
                        conversation_text += f"\nUser: {user_prompt}\nAssistant:"
                        input_text = conversation_text if scenario_type.lower() == 'chat' else user_prompt

                        print(f"Prompt: {user_prompt}")
                        print(f"Input Text: {input_text}")

                        try:
                            start_time = time.time()
                            result = subprocess.run(
                                [ollamabin, 'run', model_name, input_text, '--verbose'],
                                capture_output=True, text=True, check=True, timeout=360
                            )
                            stdout_text = result.stdout
                            stderr_text = result.stderr
                            end_time = time.time()

                            elapsed = end_time - start_time
                            new_response = stdout_text.strip()
                            output_tokens = approximate_token_count(new_response)
                            input_tokens = approximate_token_count(input_text)
                            tps = output_tokens / elapsed if elapsed > 0 else 0

                            logf.write(f"Prompt: {input_text}\n--- STDOUT ---\n{stdout_text}\n--- STDERR ---\n{stderr_text}\n")
                            print(f"Output Tokens: {output_tokens}, Elapsed Time: {elapsed:.2f}s, Tokens/s: {tps:.2f}")

                            table_data.append([
                                model_name, user_prompt, input_tokens, output_tokens, f"{elapsed:.2f}s", f"{tps:.2f}"
                            ])

                            if scenario_type.lower() == 'chat':
                                conversation_text += f" {new_response}"
                            stored_tps.append(tps)

                        except subprocess.CalledProcessError as e:
                            print(f"Error running model {model_name}: {e.stderr}")
                            logf.write(f"Subprocess Error: {e.stderr}\n")
                            continue
                        except subprocess.TimeoutExpired as e:
                            print(f"Timeout expired for model {model_name} with prompt {user_prompt}")
                            logf.write(f"Timeout expired for model {model_name} with prompt {user_prompt}\n")
                            continue
                        except Exception as e:
                            print(f"Unhandled error for model {model_name}: {str(e)}")
                            logf.write(f"Unhandled error for model {model_name}: {str(e)}\n")
                            continue

                avg_rate = sum(stored_tps) / len(stored_tps) if stored_tps else 0.0
                results[model_name] = f"{avg_rate:.2f}"
                print(f"Average Tokens/s for {model_name}: {avg_rate:.2f}")

    # Print table at the end
    print("\nBenchmark Results:")
    headers = ["Model Name", "Prompt", "Input Tokens", "Output Tokens", "Elapsed Time", "Tokens/s"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    return results

if __name__ == "__main__":
    args = parser.parse_args()
    if args.models and args.benchmark and args.type:
        benchmark_results = run_benchmark(args.models, args.benchmark, args.type, 'ollama')
        print("Final Results:", benchmark_results)

