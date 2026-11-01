.PHONY: all kernel test demo live clean
all: kernel
kernel:
	$(MAKE) -C src/kernel
test:
	python3 -m unittest discover -s tests -v
	mkdir -p build
	$(CC) -std=c11 -Wall -Wextra -Werror -fsanitize=address,undefined tests/test_math.c -o build/test_math
	./build/test_math
demo:
	python3 src/ui/server.py --mode demo
live:
	python3 src/ui/server.py --mode kernel
clean:
	rm -rf build
	$(MAKE) -C src/kernel clean
