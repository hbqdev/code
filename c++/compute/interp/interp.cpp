#include <iostream>
#include <fstream>
#include <assert.h>
#include <math.h>
//#include "Matrix.h"


double intrpf(double xi, double x[], double y[]) {
//Function to interpolate between data points
//using Lagrange polynomials (quadratic)
//inputs
//xi The x value where interpolation is computed
//x Vector of x coordinates of data points (3 values)
//y Vector of y coordinates of data points (3 values)
//output
//yi the interpolation polynomial evalued at xi

//* calculate yi = p(xi) using Lagrange polynomial
double yi = (xi - x[2]) * (xi - x[3])/((x[1]-x[2])*(x[1]-x[3]))*y[1]
  + (xi-x[1])*(xi - x[3])/((x[2]-x[1])*(x[2]-x[3]))*y[2]
  + (xi -x[1])*(xi - x[2])/((x[3]-x[1])*(x[3]-x[2]))*y[3];
return (yi);
}

int main() {
//* Initilize the data points to be fit by quadratic
double x[3+1], y[3+1];
std::cout << "Enter data points:" << std::endl;
int i;
for (i = 1; i <=3; i++) {
  std::cout << "x[" << i << "] = ";
  std::cin >> x[i];
  std::cout << "y[" << i << "] = ";
  std::cin >> y[i];
}
//* Establish the range of inerpolation( from x_min to x_max)
double x_min, x_max;
std::cout << "Enter minimum value of x: "; std::cin >> x_min;
std::cout << "Enter maximun value of x: "; std::cin >> x_max;

//*Find yi for the desired interpolation value xi using
// the function intrpl
int nplot = 100;
double *xi, *yi;
xi = new double [nplot + 1]; //Allocate memory for these
yi = new double [nplot + 1]; // arrays (nplot +1 elements)
for (i = 1; i<=nplot; i++) {
  xi[i] = x_min + (x_max-x_min) * (i-1)/(nplot-1);
  yi[i] = intrpf(xi[i],x,y); //Use intrpf function to interpolate
}
//* Print out the plotting variables: x, y, xi, yi
std::ofstream xOut("x.txt"), yOut("y.txt"), xiOut("xi.txt"), yiOut("yi.txt");
for (i = 1; i<=3; i++) {
  xOut << x[i] << std::endl;
  yOut << y[i] << std::endl;
}

for (i = 1; i <= nplot; i++) {
  xiOut << xi[i] << std::endl;
  yiOut << yi[i] << std::endl;
}

delete [] xi, yi;
return 0;
}
