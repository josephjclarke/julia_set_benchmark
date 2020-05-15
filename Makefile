bench:
	gcc -lm c.c -O0 -o no_opt_c
	gcc -lm c.c -O2 -o opt_c
	gcc -lm c.c -Ofast -o fast_c
	gfortran fortran.f95 -O0 -o no_opt_fort
	gfortran fortran.f95 -O2 -o opt_fort
	gfortran fortran.f95 -Ofast -o fast_fort
clean:
	rm no_opt_c opt_c fast_c no_opt_fort opt_fort fast_fort 
