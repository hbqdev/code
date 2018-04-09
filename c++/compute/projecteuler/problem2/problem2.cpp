#include <iostream>
using namespace std;
int a = 1;
int b = 2;
int sum = 0;
int c = a+b;
int main () {
while (c < 4000000) {
  c = a + b;
  if (c % 2 == 0) {
    sum += c;
     }
  a = b;
  b = c;
   }
cout << sum+2 << endl;
}
