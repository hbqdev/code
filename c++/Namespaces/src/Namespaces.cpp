#include <iostream>

namespace hitchhikers {
	int the_answer = 42;
}

namespace guide {
	int the_answer = 43;
}

int main() {
	std::cout << hitchhikers::the_answer << std::endl
			  << guide::the_answer << std::endl;
	return 0;
}
