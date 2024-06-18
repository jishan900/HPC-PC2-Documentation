#!/usr/bin/env python3
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os

# Check if TensorFlow can access the GPU
physical_devices = tf.config.list_physical_devices('GPU')
print("Available GPUs:", physical_devices)

# If GPUs are available, perform a simple computation
if physical_devices:
    with tf.device('/GPU:0'):
        # Create two random tensors
        a = tf.random.normal([1000, 1000])
        b = tf.random.normal([1000, 1000])
        # Perform matrix multiplication
        c = tf.matmul(a, b)
        print("Matrix multiplication result shape:", c.shape)
        
        # Convert the result to a numpy array
        c_np = c.numpy()

        # Plot the result
        plt.figure(figsize=(10, 8))
        plt.imshow(c_np, cmap='viridis')
        plt.colorbar()
        plt.title('Matrix Multiplication Result')
        plt.xlabel('Column Index')
        plt.ylabel('Row Index')

        # Save the plot temporarily if running in a batch environment
        output_directory = '/pc2/users/l/ltsbo2/Test_TF/'  # Ensure this is a writable directory
        output_file = os.path.join(output_directory, 'matrix_multiplication_result.png')
        plt.savefig(output_file)
        print(f"Plot temporarily saved as {output_file}")

print('Task Complete')
