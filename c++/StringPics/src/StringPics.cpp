#include <iostream>
#include <vector>
#include <algorithm> // for copy
#include <iterator> // for back_inserter
using namespace std;

typedef vector<string> pic;

// pic frame(const pic& p);
// pic vert_cat(const pic& top, const pic& bottom);
// pic hor_cat(const pic& left, const pic& right);

int width(const pic& v) {
	string::size_type maxlen = 0;
	for (unsigned int i = 0; i != v.size(); ++i)
		maxlen = max(maxlen, v[i].size());
	return maxlen;
}

pic vert_cat(const pic& top, const pic& bottom) {
	pic ret(top);
	copy(bottom.begin(), bottom.end(), back_inserter(ret));
	return ret;
}

