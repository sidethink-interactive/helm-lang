<table>
  <tr>
    <td align="center">
      <img src="https://github.com/sidethink-interactive/helm-lang/raw/master/logo.png" height="74">
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/sidethink-interactive/helm-lang/releases/latest">
        <img src="https://img.shields.io/badge/platforms-Windows%20|%20Linux%20|%20macOS-pink.svg">
      </a>
      <a href="https://github.com/sidethink-interactive/helm-lang/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/sidethink-interactive/helm-lang.svg">
      </a>
    </td>
  </tr>
</table>

# The Helm Programming Language

Helm is a medium-level programming language that tries to be the sanity point between C and C++. Helm embraces standardization *and* choice, so that
any Helm code should look similar to any other Helm code whilst allowing programmers to express code in whatever way is appropriate for the task at hand.

Helm is one of those things where you can learn it extremely quickly, but there's always something new you can learn about it.

```go
import std:io

main :: () {
	program := "+ + * 😃 - /";
	accumulator := 0;

	for token in program {
		switch token {
			case '+': accumulator += 1;
			case '-': accumulator -= 1;
			case '*': accumulator *= 2;
			case '/': accumulator /= 2;
			case '😃': accumulator *= accumulator;
			case: // Ignore everything else
		}
	}

	io.printf("The program \"%s\" calculates the value %d\n",
	          program, accumulator);
}
```

## Requirements to build and run

- Windows
	* x86-64
	* MSVC 2015 installed (C++11 support)
	* [LLVM binaries](https://github.com/gingerBill/Odin/releases/tag/llvm-4.0-windows) for `opt.exe` and `llc.exe`
	* Requires MSVC's link.exe as the linker
		* run `vcvarsall.bat` to setup the path

- MacOS
	* x86-64
	* LLVM explicitly installed (`brew install llvm`)
	* XCode tools installed for the linker (`xcode-select --install` will install just the tools, or you can grab XCode from the App Store)

- GNU/Linux
	* x86-64
	* Build tools (ld)
	* LLVM installed
	* Clang installed (temporary - this is calling the linker for now)

## Warnings

* This is still highly in development and the language's design is quite volatile.
* Syntax is not fixed.

## Roadmap

Not in any particular order and may never be implemented

* Compile Time Execution (CTE)
	- More metaprogramming madness
	- Compiler as a library
	- AST inspection and modification
* CTE-based build system
* Replace LLVM backend with my own custom backend
* Improve SSA design to accommodate for lowering to a "bytecode"
* SSA optimizations
* Documentation Generator for "Entities"
* Multiple Architecture support
* Debug Information
	- pdb format too
* Command Line Tooling
* Compiler Internals:
	- Big numbers library
	- Multithreading for performance increase
