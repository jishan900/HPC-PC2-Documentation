#!/bin/bash
#SBATCH -n1
#SBATCH -t 5
#SBATCH -p gpu
#SBATCH --gres=gpu:a40:1
#SBATCH --mem=45G  # Assuming 45GB is appropriate for your job, adjust as necessary
#SBATCH -q express  # Example QoS, adjust according to your needs

# Use the parallel file system for working directory
cd $PC2PFS

module reset
module load lib/TensorFlow/2.9.1-foss-2022a-CUDA-11.7.0
module load vis
module load matplotlib/3.7.0-gfbf-2022b
python /pc2/users/l/ltsbo2/Test_TF/test.py

