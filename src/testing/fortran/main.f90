PROGRAM main_test
! University of Birmingham
! Ben Palmer
Use kinds
Use MPI

IMPLICIT NONE


CALL main()

CONTAINS

! Subroutines


SUBROUTINE main()
!###########################################
! PRIVATE VARIABLES
INTEGER(kind=StandardInteger) :: i, j, k
INTEGER(kind=StandardInteger) :: steps
REAL(kind=DoubleReal) :: w(1:6)
REAL(kind=DoubleReal) :: l(1:6)
REAL(kind=DoubleReal) :: n0(1:6)
REAL(kind=DoubleReal) :: n(1:6)
REAL(kind=DoubleReal) :: source(1:6)
REAL(kind=DoubleReal) :: loss(1:6)
REAL(kind=DoubleReal) :: t_end, t_step
!###########################################

print *, "Decay Test - Po216"

w(:) = 0.0D0
w(1) = 0.2D0
w(3) = 0.07D0
w(4) = 0.005D0
w(6) = 0.01D0

l(1) = 4.683427D+00  ! 84Po216
l(2) = 1.809595D-05  ! 82Pb212
l(3) = 1.908235D-04  ! 83Bi212
l(4) = 3.777781D-03  ! 81Tl208 
l(5) = 2.310491D+06  ! 84Po212
                     ! 82Pb208

n0(:) = 0.0D0
n0(1) = 1.0D2
n0(2) = 5.0D0
n0(3) = 1.5D1
n0(6) = 3.0D2

n(:) = n0(:)

!steps = 10000000000_VeryLongInteger
t_end = 10.0D0
t_step = t_end / 1.0D10

Do k=1,10
DO i=1,1000000000
  source = 0.0D0
  loss = 0.0D0

  source(1) = t_step * w(1)
  loss(1) = n(1) * (1.0D0 - exp(-l(1) * t_step))

  source(2) = t_step * w(2) + loss(1)
  loss(2) = n(2) * (1.0D0 - exp(-l(2) * t_step))

  source(3) = t_step * w(3) + loss(2)
  loss(3) = n(3) * (1.0D0 - exp(-l(3) * t_step))

  source(4) = t_step * w(4) + 0.359300D0 * loss(3)
  loss(4) = n(4) * (1.0D0 - exp(-l(4) * t_step))

  source(5) = t_step * w(5) + 0.640700D0 * loss(3)
  loss(5) = n(5) * (1.0D0 - exp(-l(5) * t_step))

  source(6) = t_step * w(6) + loss(4) + loss(5)

  n(1:6) = n(1:6) + source(1:6) - loss(1:6)

END DO
END DO


print *, "Po216 ", n(1)
print *, "Pb212 ", n(2)
print *, "Bi212 ", n(3)
print *, "Tl208 ", n(4)
print *, "Po212 ", n(5)
print *, "Pb208 ", n(6)


END SUBROUTINE main



END PROGRAM main_test
