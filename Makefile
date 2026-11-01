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


.PHONY: help run doctor doctor-live
help:
	@echo "make demo         - дадлагын вэбийг ажиллуулах"
	@echo "make live         - бодит цөмийн вэбийг ажиллуулах (sudo шаардлагатай)"
	@echo "make kernel       - цөмийн модулиудыг бүтээх"
	@echo "make test         - Python болон C автомат тест"
	@echo "make doctor       - дадлагын орчныг оношлох"
	@echo "make doctor-live  - бодит цөмийн build орчныг оношлох"
run: demo
doctor:
	python3 tools/doctor.py
doctor-live:
	python3 tools/doctor.py --live

.PHONY: test-ui
test-ui:
	node tests/ui_smoke.cjs
