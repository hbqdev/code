#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
using namespace std;

vector<string>
split(const string& s) {
	vector<string> ret;
	unsigned int i = 0;
	while (i != s.size()) {
		// ignore leading white space
		while (i != s.size() && isspace(s[i]))
			++i;
		unsigned int j = i;
		// find end of word
		while (j != s.size() && ! isspace(s[j]))
			++j;
		// copy the characters in the range [i,j)
		if (i != j) {
			ret.push_back(s.substr(i, j - i));
			i = j;
		}
	}
	return ret;
}

bool space(char c) {
	return isspace(c);
}
bool not_space(char c) {
	return !isspace(c);
}

// alternative implementation using standard algorithms
vector<string>
split2(const string& s) {
	typedef string::const_iterator iter;
	vector<string> ret;
	iter i = s.begin();
	while (i != s.end()) {
		// ignore leading white space
		i = find_if(i, s.end(), not_space);
		// find end of word
		iter j = find_if(i, s.end(), space);
		// copy the characters in the range [i,j)
		if (i != s.end())
			ret.push_back(string(i, j));
		i = j;
	}
	return ret;
}

int main() {
	string s;
	while (getline(cin, s)) {
		vector<string> v = split2(s);
		for (unsigned int i = 0; i != v.size(); ++i)
			cout << v[i] << endl;
	}
	return 0;
}
