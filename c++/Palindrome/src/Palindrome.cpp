#include <iostream>
#include <string>
using namespace std;

string reverse(string s) {
   int n = s.size();
   for (int i = 0; i != n / 2; ++i)
      swap(s[i], s[n-i-1]);
   return s;
}

int main() {
   cout << "If you type in a word, I'll tell you if it is"
         " a palindrome." << endl;
   string w;
   cin >> w;
   string w_rev = reverse(w);
   if (w == w_rev)
      cout << "Yes, " << w << " is a palindrome." << endl;
   else
      cout << "No, " << w << " is not a palindrome." << endl;
   return 0;
}
