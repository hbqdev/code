#include <iostream>
#include <iomanip> // for setw
#include <vector>
#include <algorithm> // for max and sort
#include <stdexcept> // for domain_error
#include <assert.h>
using namespace std;

// Functions from OrganizingPrograms

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

// Note, changed to add an "if" and clear.
istream& read_homework(istream& in, vector<double>& homework) {
   if (in) {
	   double x;
	   homework.clear();
	   while (cin >> x)
		   homework.push_back(x);
	   in.clear(); // clear the error state
   }
   return in;
}

// New structure for grouping student information.

struct student_info {
	string name;
	double midterm, final;
	vector<double> homework;
};

istream& read(istream& in, student_info& s) {
	in >> s.name >> s.midterm >> s.final;
	return read_homework(in, s.homework);
}

double grade(const student_info& s) {
	return grade(s.midterm, s.final, s.homework);
}

bool compare_names(const student_info& s1, const student_info& s2) {
	return s1.name < s2.name;
}

int main() {
	vector<student_info> students;
	student_info student;
	string::size_type maxlen = 0;
	while (read(cin, student)) {
		maxlen = max(maxlen, student.name.size());
		students.push_back(student);
	}
	sort(students.begin(), students.end(), compare_names);
	for (unsigned int i = 0; i != students.size(); ++i) {
		cout << setw(maxlen+1) << students[i].name;
		try {
			double course_grade = grade(students[i]);
			streamsize old_prec = cout.precision(3);
			cout << " " << course_grade << endl;
			cout.precision(old_prec);
		} catch (const domain_error& e) {
			cout << e.what();
		}
	}
	return 0;
}
