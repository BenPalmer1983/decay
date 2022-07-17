mpif90 -g \
-fopenmp \
-fbounds-check \
-mtune=native \
kinds.f90 \
main.f90 \
-o test.x \
&& ./test.x
