#!/bin/bash
w=1
echo $w
export w
job_id_array=$(sbatch --job-name=Gen_${w} run_array.sh)
echo ${job_id_array##* }
job_id=$(sbatch  --job-name=${w}_Comparison --dependency=afterany:${job_id_array##* } comp_pert.sh)
echo ${job_id##* }


for w in {2..10}
do
    echo $w
    export w
    job_id_array=$(sbatch --job-name=Gen_${w}  --dependency=afterany:${job_id##* } run_array.sh)
    echo ${job_id_array##* }
    job_id=$(sbatch  --job-name=${w}_Comparison --dependency=afterany:${job_id_array##* } comp_pert.sh)
    echo ${job_id##* }
done
