dir_path='/scratch/er691/AEMG/examples'

system='ndpendulum'
underline='_'
control='lqr'

python $dir_path/generate_config.py --config $system.txt


k="000"
w="k"


for i in 1 10 100
do
    python $dir_path/get_data.py --num_trajs "$i$k" --save_dir "data/$system$underline$control$i$w/"
done

python run.py --system ndpendulum --control lqr

