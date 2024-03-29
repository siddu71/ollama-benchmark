import typer
from llm_benchmark import check_models
from llm_benchmark import check_ollama
from llm_benchmark import run_benchmark

from systeminfo import sysmain

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}!")
    

@app.command()
def run(sendinfo: bool = True):
    sys_info = sysmain.get_extra()
    print(f"Total memory size : {sys_info['memory']:.2f} GB") 
    print(f"cpu_info: {sys_info['cpu']}")
    print(f"gpu_info: {sys_info['gpu']}")
    print(f"os_version: {sys_info['os_version']}")

    check_ollama.check_ollama_version()
    print('-'*10)

    ft_mem_size = float(f"{sys_info['memory']:.2f}")
    models_file_path = 'data/benchmark_models_16gb_ram.yml'
    if(ft_mem_size>=4 and ft_mem_size <7):
        models_file_path = 'data/benchmark_models_4gb_ram.yml'
    elif(ft_mem_size>=7 and ft_mem_size <15):
        models_file_path = 'data/benchmark_models_8gb_ram.yml'

    check_models.pull_models(models_file_path)
    print('-'*10)

    benchmark_file_path = 'data/benchmark1.yml'

    bench_result_info = {}
    result1 = run_benchmark.run_benchmark(models_file_path,benchmark_file_path, 'instruct')
    bench_result_info.update(result1)
    result2 = run_benchmark.run_benchmark(models_file_path,benchmark_file_path, 'question-answer')
    bench_result_info.update(result2)
    result3 = run_benchmark.run_benchmark(models_file_path,benchmark_file_path, 'vision-image')
    bench_result_info.update(result3)

    if (sendinfo==True):
        print(f"Sending the following data to a remote server")
        print(f"Your machine UUID : {sysmain.get_uuid()}")
        print(f"{bench_result_info.items()}")
        print('=='*10)
        print(f"{sys_info.items()}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Mr.(Ms.) {name}. Have a good day.")
    else:
        print(f"Bye {name}!")

@app.command()
def sysinfo(formal: bool = True):
    if formal:
        sys_info = sysmain.get_extra()
        #print(sys_info.items())
        print(f"Total memory size : {sys_info['memory']:.2f} GB") 
        print(f"cpu_info: {sys_info['cpu']}")
        print(f"gpu_info: {sys_info['gpu']}")
        print(f"os_version: {sys_info['os_version']}")
        print(f"Your machine UUID : {sysmain.get_uuid()}")
        print()
    else:
        print(f"No print!")


if __name__ == "__main__":
    app()
