---
blogpost: true
date: 2022-07-25
tags: ["c","posix"]
category: Blog
author: myself
---

# C language Notes

## --- Part I - C ---

## Preprocess 

Happens on one translation unit

#### Define 

```
#define X Y
#undef X
```

In this translation unit, replace all X with Y

```
gcc -E -> preprocess result
gcc -g3 -> include macros in debugger
```

#### Example

```c
#define ARCH_DIR x86_64
#define ARCH(bar) <ARCH_DIR/bar>

#include ARCH(blarg.h)
```

This also works if swtich line 1 and 2.

### Include 

```
#include <foo.h> -> usually search in stdlib location
#include "foo.h" -> usually search in file directory, then search in stdlib location
```

read foo.h, process it, and inline it here

## Compile and Link

### File Types

```
.c -> code text
.o -> object ELF
.a -> archive 
.so -> dynamic lib ELF
```

### Tools

```
Compiler -> gcc
Static Linker 
Dynamic Linker -> os
```

### Gcc Options

```
-o -> output executable
-l -> dynamic linking
-I -> inlclude directory 
-D -> define preprocess variables
-O2 -> optimization level

```

### Include Location Search Order

```
-I dir
-iquote dir
-isystem dir
-idirafter dir
```

1.  For the quote form of the include directive, the directory of the current file is searched first.
2.  For the quote form of the include directive, the directories specified by -iquote options are searched in left-to-right order, as they appear on the command line.
3.  Directories specified with -I options are scanned in left-to-right order.
4.  Directories specified with -isystem options are scanned in left-to-right order.
5.  Standard system directories are scanned.
6.  Directories specified with -idirafter options are scanned in left-to-right order.

Source : https://gnu.huihoo.org/gcc/gcc-9.3.0/gcc/Directory-Options.html#Directory-Options

## Main

Only two correct mains

```
int main(void)
int main(int argc, char* argv[])
```

## Declaration vs Definition

```
// declaration
extern int a;
int foo(int b);

// definition : allocates storage for an entity
int a;
int foo(int b) {}
```

All definitions are implicitly declarations. 

A declaration is also a definition unless:

- declare function without a body
- contains the 'extern' keyword
- is a typedef

An entity must be defined exactly once (in a translation unit if the entity has internal linkage; in the entire program if the entity has external linkage).

### External Variables Definition vs Declaration

- Inititializer == Yes

  Makes the statement a definition (and a declaration

- Initializer == No && extern == Yes

  Makes the statement a declaration only (with external linkage)

- Initializer == No && (extern == No or Static == Yes)

  A tentative definition (which acts as a definition with the initializer `= 0` or `= {0}` if there is no definition in the same translation unit)		

```c
  // A declaration with external linkage
  extern int i;  

  // A definition with external linkage
  int total = 0; 

  // A definition with internal linkage
  static const char *university = "JMU";

  // A tentative definition with external linkage
  int  j;

  // A tentative definition with internal linkage
  static int k;
```

## Scope & Linkage & Storage Duration

### Scope

The portion of a translation unit (i.e., the code produced by the preprocessor from the source file and the header files) in which an identifier is visible (i.e., represents an entity) 

- file
- block
- function prototype

### Storage duration

The (minimum potential) lifetime of the storage containing an entity

- static
- automatic
- allocated

|            | **Block Scope** | File Scope |
| --- | -------- | --- |
| None       | Automatic       | Static     |
| `auto`     | Automatic       | N/A        |
| `extern`   | Static          | Static     |
| `register` | Automatic       | N/A        |
| `static`   | Static          | Static     |

### Linkage

Determines whether declarations in different scopes can refer to the same entity

- No Linkage

  The entity can't be referenced by name from anywhere else

- Internal

  The entity can be referenced by names declared in the same scope and/or names declared in other scopes of the same translation unit

- External

  The entity can also be referenced by name in other translation units

| Functions  | **Block Scope** | File Scope |
| --- | -------- | --- |
| None       | External*       | External*  |
| `auto`     | N/A             | N/A        |
| `extern`   | External*       | External*  |
| `register` | N/A             | N/A        |
| `static`   | N/A             | Internal   |

Function definition and declaration must agree on Linkage Options.

| Variables  | **Block Scope** | File Scope |
| --- | -------- | --- |
| None       | No Linkage      | External   |
| `auto`     | No Linkage      | N/A        |
| `extern`   | External\*      | External\* |
| `register` | No Linkage      | N/A        |
| `static`   | No Linkage      | Internal   |

\*External Linkages in the table are true unless it was previously (visibly) declared with internal linkage. 

## Variable Types

```
char c;
short s;
int i;
long l;

```

## Inititalizer

```
struct Person p = {}; // init all to zero
struct Person p = {.name="Michael"}; // init name, others to zero
```

## Function Parameter Types

```
int foo()
	int a;
	int b;
	{
	 	reutrn a * b;
	}
```

```
foo() -> empty identifier list
bar(void) -> takes no parameters

foo(5) -> emit warning
bar(5) -> err too many arguments
```

## Rounding

```
// for x/n
x/n -> floor
(x+n-1)/n -> ceil
(x+n/2)/n -> nearest integer
(x+n-1) & ~(n-1) -> nearest multiple of n
```

## ---  Part II - POSIX ---

## File Operations

### File Types

- Buffered and Unbuffered
- Regular File
- Directory
- Symbolic Link
- Named Pipe
- Socket
- Device/Special File
  - Character device
  - Block Device

### Operations

- Open, read, write, close
- umask, fchmod, fchown
- fstat, fcntl
- lock

```c
int fd = open("foo.txt", O_RDONLY);
int num_read = read(fd, pBuf, num_to_read);
close(fd);
```

| Descriptor | <unistd.h>              | <stdio.h>    |
| --- | --------- | ----- |
| 0          | #define STDIN\_FILENO 0 | FILE\* stdin |
| 1          | #define STDOUT\_FILENO 1| FILE\* stdout|
| 2          | #define STDERR\_FILENO 2| FILE\* stderr|

```c
FILE * fdopen(int fd);
int fileno(FILE* stream);
```

### Descriptor vs Stream

Stream automatically supports buffering input and output. 

```c
sync(void); // for all descriptors
syncfs(int fd);
```

## Lifetime of a File

open vs unlink

```c
creat(file_name);
// same as
open(file_name, O_CREAT|O_WRONLY|O_TRUNC);
```

```
remove()
// same as
unlink()
// ro
rmdir()
```

### Directory

```c
DIR* opendir(char* dir_path);
readdir() // get next directory entry
telldir() // current position
seekdir() // move position
rewinddir() // move position to beginning
closedir() // close
chdir()/pwd
rmdir
```

```c
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <unistd.h>
#include <stdio.h>

int main(void) {
	DIR* d = opendir(".");
    while (1) {
        struct dirent * de = readdir(d);
        if (de == NULL) break;
        struct stat s;
        stat(de->d_name, &s);
        printf("%-20s %6.6o, %7ld\n", 
              de->d_name, s.st_mode, s.st_size);
    }
    closedir(d);
    return 0;
}
```

## Memory

Default on demand paging. Can override with `mlock`, to lock a contiguous part of VA in physical memory. 

### mmap

```
PROT_(READ|WRITE|EXEC|NONE)
MAP_PRIVATE
MAP_SHARED
MAP_ANONYMOUS
MAP_FIXED

```

 changing contents of file

Option 1: open, read, modify, write, close

Option 2:

```
int fd = open("log.txt", O_RDWR);
struct stat st;
fstat(fd, &st);
unsigned file_size = st.st_size;
char* p = mmap(NULL, file_size, PROT_READ|PROT_WRITE, MPA_SHARED, fd, 0);
p[1] = 'e';
munmap(p.file_size);
close(fd);
```

## System Information

```
sysconf
sysinfo
pathconf
(get|set)_rlimit
confstr
getconf
```

## Signals

Aka software interrupts

synchronously - by code executing in process

asynchronously - by process to process

```
kill -s 0 <pid> // check if pid is valid pid
```

## Lifetime management

Automatic variables

atexit functions

pthread_once

init mutex

static variables

\_\_constructor\_\_

## ELF extrainfo

- header
- Segment mapping
- Symbol table

DWARF debug info

Use `strip` to remove those debug info, significantly reduce executable size

## Typed Memory

## Potential Problems

- forgot to close files (not flushed to disk)
- fork bomb
- session leader

## --- Part III - Undefined Behavious ---

Reference : https://blog.regehr.org/archives/213

