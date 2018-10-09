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

Helm is a pretty simple language, but its details allow programmers to implement complex interconnected systems with little to no fuss, unline
a comparable project in C or C++. Helm is **not** garbage-collected, and never will be. Nor does Helm provide complex ownership syntax like Rust - instead, it makes manual memory management simple, intuitive, and clear. You'll have to remember to `free` things, but you get bare-metal performance and frictionless iteration in place of memory management.

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

**Helm is heavily inspired by [Odin](https://github.com/odin-lang/Odin).** The Helm compiler is 100% written from scratch, but the design is in some ways based on the Odin compiler's internals. Additionally, the syntax of Helm is based on Odin's and Jai's syntax.

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

## Roadmap

Not in any particular order and may never be implemented

* Compile test program
* Add very basic class system (constructors and deconstructors)
* Operator overloading in classes
* Start writing standard library
* Output debugging symbols
* Create custom codegen backend (maybe? Do I need the speed this will provide?)
* Implement JIT (for metaprogramming)
* Create nice JIT API
* Implement #compile directive to function like #foreign_system_library, but with C source code
* Compatability with C++ function signatures
* Compatability with ObjC function signatures...?
* (zachary): Write sample game engine
* Multithreaded compiler?
* Code optimizations