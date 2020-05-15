integer function escapes(z)
  implicit none
  complex,intent(in) :: z
  complex :: z0
  z0 = z
  do escapes = 1,100
     z0 = z0 * z0 - (0.5,0.0)
     if (abs(z0) .GT. 50.0) then
        return
     end if
  end do
  escapes = 0
  return
end function escapes


program julia
  implicit none
  integer :: x,y,b,i
  complex :: z
  integer::escapes
  open(unit=10,file="set.ppm",action="write")

  write(10,"(A2)") "P3"
  write(10,"(A9)") "5000 5000"
  write(10,"(A3)") "255"
  
  do y = 5000,1,-1
     do x = 1,5000
        z = (4.0 / 5000) * CMPLX(x,y) - (2.0,2.0)
        i=escapes(z)
        if (i .EQ. 0) then
           write (10,*) "255 255 255 "
        else
           b = 255 * i / 100
           write (10,*) "0 ",b,b," "
        end if
     end do
  end do
end program julia
