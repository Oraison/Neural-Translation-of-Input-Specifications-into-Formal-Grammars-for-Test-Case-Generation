# echo "$1"
# conda activate dogyu

if [ $# -ge 2 ]; then
    declare -i num_variable=$2
else
    declare -i num_variable=20
fi
# for i in {0..$num_variable..1}
for ((i = 0; i < $num_variable; i++))
    do 
        echo "$1_res$i"
        python add_spec_generated.py "$1_res$i"
        python test_generated.py "$1_res$i"
    done
