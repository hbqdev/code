#include <iostream>
#include <math.h>
using namespace std;

int main () {
float prime;
float i = 0;
float greatprime;
cout << "Enter the prime number:";
cin >> prime;

while (i < prime) {
  if (fmod(prime, i)  == 0){
   greatprime = i;

}
i++;
}
  cout << greatprime << endl;

}
