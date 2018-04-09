#include <iostream>

using namespace std;
int a = 0;
int main ()
{
  for(int n = 1; n<1000; n++) {
    if (n % 3 == 0 | n % 5 == 0) {
      a += n; }
}
  cout << a <<endl;
}
