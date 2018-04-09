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
return y(i);
}
