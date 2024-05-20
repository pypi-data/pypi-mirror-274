
build:
	maturin build

install: build
	pip install -e .

cross-build:
	maturin build --release --target aarch64-unknown-linux-gnu --zig -i python3.10

build-all: build cross-build

publish:
	maturin publish