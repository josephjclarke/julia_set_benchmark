#include <stdio.h>
#include <complex.h>

#define max_real 2.0
#define max_imag 2.0
#define number 5000
#define max_radius 50.0
#define iters 100

unsigned int iterate_until_escape(double complex z);
void to_rgb(unsigned int i,char* buf);

int main(int argc, char **argv)
{
  FILE *file;
  double incr;
  int x,y;
  char buf[13];
  complex double z;
  incr = 2*max_imag / number;

  file = fopen("set.ppm","w");
  fprintf(file,"P3\n%d %d\n255\n",number,number);
  for(y = number; y > 0; y--){
    for(x =  0;  x < number; x++) {
      z = (2.0 * max_imag / number) * (x + I * y) - (2.0 + 2.0*I);
      to_rgb(iterate_until_escape(z),buf);
      fputs(buf,file);
    }
  }
  fclose(file);
  return 0;
}

void to_rgb(unsigned int i,char* buf)
{
  unsigned int b;

  if (i == 0) {
    sprintf(buf,"255 255 255 ");
  }
  else {
    b = 255 * i / iters;
    sprintf(buf,"0 %u %u ",b,b);
  }
}

unsigned int iterate_until_escape(double complex z)
{
  unsigned int i;
  for (i = 1; i < iters; i++){
    z = z*z - 0.5;
    if (cabs(z) > max_radius) {
      return i;
    }
  }
  return 0;
}
