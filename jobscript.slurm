#!/bin/bash -l
#SBATCH --account=lp_h_ds_students
#SBATCH --cluster=genius
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00

conda activate cds-ternary-search-tree
python -m src.benchmarks.benchmark_ternary_search_tree
