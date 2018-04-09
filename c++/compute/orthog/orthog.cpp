//orthog-Program to test if a pair of vectors
//is orthogonal. Assumes Vectors are in 3D space
#include <iostream>

int main() {
//* Initialize the vectors a and b
double a[3+1], b[3+1];
std::cout << "Enter the first vector" << std::endl;
int i;
for (i=1; i<=3; i++) {
  std::cout << " b[ "<< i << "] = ";
  std::cin >> b[i];
}

//*Evaluate the dot product as sum over products of elements
double a_dot_b = 0.0;
for (i = 1; i<=3; i++){
 a_dot_b += a[i]*b[i];
}
//*Print dot product and state whether vectors are orthogonal
if (a_dot_b == 0.0)
 std::cout << "vectors are orthogonal " << std::endl;
else {
std::cout <<  "Vectors are NOT Orthogonal" << std::endl;
std::cout << "Dot products = " << a_dot_b << std::endl; 
}
return 0;
}
