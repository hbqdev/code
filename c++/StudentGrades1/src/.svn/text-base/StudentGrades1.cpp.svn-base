#include <iostream>
using namespace std;

int main() {
   cout << "Please enter your midterm and "
		   "final exam grades: ";
   double midterm, final;
   cin >> midterm >> final;
   cout << "Enter all your homework grades, "
         "followed by end-of-file: ";
   int count = 0;
   double sum = 0;
   double x;
   while (cin >> x) {
	  ++count;
      sum += x;
   }
   // Print three significant digits.
   streamsize prec = cout.precision(3);
   cout << "Your course grade is "
       << 0.2 * midterm + 0.4 * final + 0.4 * sum / count
       << endl;
   cout.precision(prec);
   return 0;
}
