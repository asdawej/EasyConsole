# EasyConsole

A console easy to use.

Here, you can use number or your customized symbols to represent a long and ugly directory/file path.

These is the command we support:

- `help [<Topic :: str>]`
  - Helper.
- `hello [<Name :: str>]`
  - To say hello. You can attach a name to it.
- `exit [<Name :: str>]`
  - To exit console. You can attach a name to it.
- `cd [<Path :: int | const | val>]`
  - To open and move to a directory. If not given any argument, it will open the current directory, like `cd .` in cmd.
- `ls [<Path :: int | const | val>]`
  - To list out the paths under a directory. If not given argument, it will list out the current directory.
- `const <ConstAlias :: str> <Path :: int | const | val>`
  - To give a path with a constant alias. Constant alias still valid the next time you use this console.
- `let <ValAlias :: str> <Path :: int | const | val>`
  - To give a path with a temporary alias. It will not be kept after you exit the console.
- `del <Alias :: str> [<Set = const | let>]`
  - To delete an alias. If not given the set, we will find it first in the set of temporary aliases then the set of constant aliases.
- `run <SymCmd :: line(str, int, const, val)>`
  - To run a command line. All the numbers and aliases valid will be replaced.
- `cmd <RawCmd :: line(str)>`
  - To run a command line in its raw state.
