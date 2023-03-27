dir_path='/scratch/er691/AEMG/example'

python $dir_path/generate_config.py --config ndpendulum.txt

system='ndpendulum'
underline='_'
control='lqr'


k="000"
w="k"


for i in 1 10 100
do
    python $dir_path/get_data_map.py --num_trajs "$i$k" --save_dir "data/$system$underline$control$i$w/"
done

python run.py --system ndpendulum --control lqr

