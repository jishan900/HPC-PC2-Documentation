import tensorflow as tf
import numpy as np
import scipy
import ray
import click
import gym
import tqdm
import joblib
import progressbar
import zmq
import cloudpickle
from mpi4py import MPI
import os
import sys
import time

def check_tensorflow_cuda():
    print("TensorFlow CUDA support: ", tf.test.is_built_with_cuda(), flush=True)
    print("Available GPUs: ", tf.config.list_physical_devices('GPU'), flush=True)

def check_numpy():
    print("NumPy version: ", np.__version__, flush=True)

def check_scipy():
    print("SciPy version: ", scipy.__version__, flush=True)

def check_ray():
    ray.init(ignore_reinit_error=True)
    print("Ray is running", flush=True)

def check_click():
    @click.command()
    def hello():
        click.echo('Hello, Click!')
    hello(["--help"])

def check_gym():
    env = gym.make("CartPole-v1")
    print("Gym environment created: ", env, flush=True)

def check_tqdm():
    for i in tqdm.tqdm(range(100)):
        pass
    print("tqdm works", flush=True)

def check_joblib():
    from joblib import Parallel, delayed
    import time
    def slow_function(i):
        time.sleep(0.1)
        return i
    results = Parallel(n_jobs=2)(delayed(slow_function)(i) for i in range(5))
    print("Joblib results: ", results, flush=True)

def check_progressbar2():
    bar = progressbar.ProgressBar(max_value=10)
    for i in range(10):
        bar.update(i)
    print("progressbar2 works", flush=True)

def check_zmq():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.bind("tcp://*:5555")
    print("ZeroMQ socket bound to port 5555", flush=True)

def check_cloudpickle():
    pickled = cloudpickle.dumps(lambda x: x**2)
    unpickled = cloudpickle.loads(pickled)
    print("cloudpickle works: ", unpickled(2), flush=True)

def check_mpi4py():
    comm = MPI.COMM_WORLD
    print("MPI4py initialized with size: ", comm.Get_size(), flush=True)
    print("MPI rank: ", comm.Get_rank(), flush=True)

def main():
    try:
        check_tensorflow_cuda()
    except Exception as e:
        print("Error in TensorFlow: ", e, flush=True)
        
    try:
        check_numpy()
    except Exception as e:
        print("Error in NumPy: ", e, flush=True)
    
    try:
        check_scipy()
    except Exception as e:
        print("Error in SciPy: ", e, flush=True)
    
    try:
        check_ray()
    except Exception as e:
        print("Error in Ray: ", e, flush=True)
    
    try:
        check_click()
    except Exception as e:
        print("Error in Click: ", e, flush=True)
    
    try:
        check_gym()
    except Exception as e:
        print("Error in Gym: ", e, flush=True)
    
    try:
        check_tqdm()
    except Exception as e:
        print("Error in tqdm: ", e, flush=True)
    
    try:
        check_joblib()
    except Exception as e:
        print("Error in joblib: ", e, flush=True)
    
    try:
        check_progressbar2()
    except Exception as e:
        print("Error in progressbar2: ", e, flush=True)
    
    try:
        check_zmq()
    except Exception as e:
        print("Error in ZeroMQ: ", e, flush=True)
    
    try:
        check_cloudpickle()
    except Exception as e:
        print("Error in cloudpickle: ", e, flush=True)

    try:
        check_mpi4py()
    except Exception as e:
        print("Error in MPI4py: ", e, flush=True)
    
    print("Successfully checked all libraries", flush=True)
    sys.stdout.flush()  # Ensure all output is flushed
    time.sleep(2)  # Add a delay to ensure the message is printed before the process ends

if __name__ == "__main__":
    # Set PSM2_CUDA environment variable based on warning from Open MPI
    os.environ['PSM2_CUDA'] = '1'
    
    main()
