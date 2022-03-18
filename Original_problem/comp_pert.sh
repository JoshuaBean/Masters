#!/bin/bash
#SBATCH --job-name={$w}_comparing
#SBATCH --output=./Slurms/Comparing_%j.out
#SBATCH -A rc005
#SBATCH -p batch				# QUEUE job will be added to
#SBATCH -N 1
#SBATCH -n 2					# Number of cores (max 32)
#SBATCH --time=00-00:15:00			# Time length of code in (D-HH:MM:SS)
#SBATCH --mem=4GB				# Memory allowed per cores

# Notifications
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=joshua.bean@adelaide.edu.au




newgrp a1705663

module load Python/3.7.0
module load Anaconda3/2020.07

python INSH.py $w
