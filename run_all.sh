for num_tellers in 2 3; do
	for lunch_break_length in 0.75 1; do
		python bank_sim.py $lunch_break_length $num_tellers
	done
done
