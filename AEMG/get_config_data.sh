dir_path='/scratch/er691/AEMG/examples'

system='ndpendulum'
underline='_'
control='lqr'

cd $dir_path
python generate_config.py --config $system.txt


k="000"
w="k"


for i in 1 10 100
do
    python get_data.py --num_trajs "$i$k" --save_dir "/data/$system$underline$control$i$w/" --system 'ndpendulum'
done

cd '/scratch/er691/Tripods-Amarel/AEMG'
python run.py --system ndpendulum --control lqr

