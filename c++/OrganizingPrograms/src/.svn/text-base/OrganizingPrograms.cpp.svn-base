#include <iostream>
#include <algorithm> // for sort
#include <vector>
#include <assert.h>
#include <stdexcept> // for domain_error
using namespace std;

double median(const vector<double>& v) {
   if (v.size() == 0)
      throw domain_error("can't compute median of empty vector");
   vector<double> v2(v);
   sort(v2.begin(), v2.end());
   int mid = v2.size() / 2;
   double median;
   if (v2.size() % 2 == 0)
      median = (v2[mid - 1] + v2[mid]) / 2;
   else
      median = v2[mid];
   return median;
}

double grade(double midterm, double final,
           const vector<double>& homework) {
   try {
      return 0.2 * midterm + 0.4 * final + 0.4 * median(homework);
   } catch (domain_error& e) {
      throw domain_error("need at least one homework");
   }
   return 0; // to quiet the warning
}

void read_homework(istream& in, vector<double>& homework) {
   assert(in != false);
   assert(homework.size() == 0);
   double x;
   while (cin >> x)
      homework.push_back(x);
   in.clear(); // clear the error state
}

int main() {
   cout << "Please enter your midterm and final exam grades: ";
   double midterm, final;
   cin >> midterm >> final;
   cout << "Enter all your homework grades, "
           "followed by end-of-file: ";
   vector<double> homework;
   read_homework(cin, homework);
   try {
      double course_grade = grade(midterm, final, homework);
      streamsize prec = cout.precision(3);
      cout << "Your course grade is " << course_grade << endl;
      cout.precision(prec);
   } catch (domain_error& e) {
      cout << e.what() << endl;
   }
   return 0;
}
