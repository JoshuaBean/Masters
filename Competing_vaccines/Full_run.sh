#!/bin/bash
#SBATCH --job-name=Comparing
#SBATCH --output=./Slurms/Running_%A_%a.out
#SBATCH -A rc005
#SBATCH --array=1-64
#SBATCH -p batch				# QUEUE job will be added to
#SBATCH -N 1
#SBATCH -n 32					# Number of cores (max 32)
#SBATCH --time=00-12:00:00			# Time length of code in (D-HH:MM:SS)
#SBATCH --gres=tmpfs:4G
#SBATCH --mem=40GB				# Memory allowed per cores


newgrp a1705663

module load Python/3.7.0
module load Anaconda3/2020.07

python trial_designs.py ${SLURM_ARRAY_TASK_ID}
