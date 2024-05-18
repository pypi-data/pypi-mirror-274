# magnetsting
_Create command-line projects with ease._

MagnetSting is a framework written in Python that simplifies the creation of command-line projects. It comes with various 
capabilities built into it, such as help banner creation, command aliasing, shell-like behaviour and more. It is built using 
modules only from the standard library and can run on Linux-based machines without any additional dependencies. 

<!-- Note about compatibility -->
> [!NOTE]
> Currently, MagnetSting can only operate on Linux-based machines. However, work is being done to make it compatible with 
> Windows-based machines as well.

<!-- Installation -->
## Installation
MagnetSting can be installed from PyPI using pip: `pip3 install magnetsting`.

<!-- Commands -->
## Commands
MagnetSting allows for the creation of three types of commands: `single-`, `args-` and `file-type` commands. The order in which 
the commands are created determines the order they appear in the help banner. Command names can contain letters, numbers and 
symbols. What a command name cannot contain however is a space due to the way that MagnetSting parses commands.

<!-- Single-type Commands -->
### Single-type Command
Single-type commands consist of only a command name that, when called, executes the function assigned to it. Anything 
typed after the command name is not passed on to the function and has no affect on the command.

Create a single-type command:
```python
from magnetsting import MagnetSting

mast = MagnetSting()

def mysinglefunction(additional_data: tuple = None):
    print("foo bar baz")

mast.add_command_type_single(command_name="mysinglecommand", command_help="short description of mysinglecommand",
                             command_group=None, command_function=mysinglefunction, additional_data=None)

mast.magnetsting_mainloop()
```

Call a single-type command:
`mysinglecommand`

<!-- Required parameter -->
> [!IMPORTANT]
> Functions assigned to single-type commands **must** have the following parameter:
> `additional_data: tuple = None`. The `additional_data` parameter is anything that needs to be passed to the 
> function in the form of a tuple. The `additional_data` parameter can be useful if you are using an instance of
> MagnetSting within another instance.

<!-- Args-type Commands -->
### Args-type Commands
Args-type commands differ from single-type commands by being able to take arguments after the command name. Anything 
typed after the command name is then passed on in the form of a `list` to the function assigned to the command. If 
nothing is typed after the command name, a message will be displayed indicating that an argument is required. 

Create an args-type command:
```python
from magnetsting import MagnetSting

def myargsfunction(command_args: list = None, additional_data: tuple = None):
    for commands in command_args:
        print(commands)    

mast = MagnetSting()
mast.add_command_type_args(command_name="myargscommand", command_help="short description of myargscommand", 
                           command_group=None, command_function=myargsfunction, additional_data=None)

mast.magnetsting_mainloop()
```

Call an args-type command:
`myargscommand foo bar baz`

<!-- Required parameters -->
> [!IMPORTANT]
> Functions assigned to args-type commands **must** have the following parameters:
> `command_args: list = None, additional_data: tuple = None`. The `command_args` parameter is for the argument
> list while the `additional_data` parameter is anything else that needs to be passed to the function in the
> form of tuple. The `additional_data` parameter can be useful if you are using an instance of MagnetSting within
> another instance. 

<!-- File-type Commands -->
### File-type Commands
File-type commands differ from `single-` and `args-type` commands by executing Python files rather than call on functions. 
This command is more geared towards files that can take arguments in the command-line, such as those that use the 
"argparse" or "click" modules, but there is no restriction that would prohibit one from assigning a Python file that 
does not take arguments. Arguments can be passed by typing them after the command name, just like with `args-type` 
commands. For example, assume that the command name `mycommand` has the file `myfile.py` assigned to it. Assuming it 
was created using "argparse", you could call the help banner by typing `mycommand --help`. A file assigned to a 
file-type command does not need to be in the same project directory, it can be anywhere on a system. If the file is 
located somewhere other than the project directory, make sure to include the full or relative path when adding it to
`command_file` parameter.

Create a file-type command:
```python
from magnetsting import MagnetSting

mast = MagnetSting()
mast.add_command_type_file(command_name="myfilecommand", command_help="short description of myfilecommand",
                           command_group=None, command_file="command.py")

mast.magnetsting_mainloop()
```

Call a file-type command:
`myparsercommand --help` 

<!-- Command Groups -->
## Command Groups
Command groups are, as the name suggests, groups that commands can be assigned to. It offers a way to organize
commands together and to keep the main help banner from becoming too long and overwhelming. Any command assigned to
a command group will not show up in the main help banner, rather, the command group name will show instead. A command
group must be created **prior** to adding any commands to it. Otherwise, an exception will be raised. The syntax to call a 
command in a command group is the following: `<command group name> <command name> <args (if args- or file-type)>`.
To view all the commands in a group, just call the command group's name. If you do not want to assign a command to a 
command group, just leave the `command_group` parameter as "None" (the default value). Just like command names, command group
names can contain letters, numbers and symbols but not spaces.

Create a command group and add a command to the group:
```python
from magnetsting import MagnetSting

def myfunc(additional_data: tuple = None):
    print("foo bar baz")

mast = MagnetSting()

mast.add_command_group(group_name="mygroup", group_help="short description of mygroup")

mast.add_command_type_single(command_name="mycommand", command_help="short description of mycommand", 
                             command_group="mygroup", command_function=myfunc, additional_data=None)

mast.magnetsting_mainloop()
```

Call a command in a command group:
`mygroup mycommand`

View all available commands in a command group:
`mygroup`

<!-- magnetsting_mainloop Method -->
## magnetsting_mainloop Method
The `magnetsting_mainloop()` method is the core of MagnetSting. It handles all of its operations, from the parsing 
of commands to the creation of the help banner. Once you have created all of your commands and command groups, call this
method and ta-da, your project is now fully functional :tada:.

<!-- Command Aliases -->
## Command Aliases
Commands can also be aliased. Rather than have to type a lengthy command and its arguments over and over again, a short alias of 
the command can be created. All types of commands, including commands within command groups and even alias commands, can be 
aliased. By default, all aliases are written to a JSON file called ".alias.json". The file resides in the same directory as the 
project. However, the file can be renamed and reside elsewhere, the value just needs to be modified in the class initialization 
through the `alias_file` parameter. If the alias file resides somewhere other than the project directory, include the absolute or 
relative path. While the JSON file can be edited outside of MagnetSting, it is recommended to make any changes within MagnetSting 
as there are guards in place to prevent creating aliases of commands that do not exist or creating an alias name the same as an 
existing command name. Aliased `args-` and `file-type` commands can also have arguments added onto an existing alias. For example, 
assume that the args-type command `myargs arg1 arg2 arg3` is aliased as `myalias`. You can add arguments when calling the aliased 
command by typing them after the alias name: `myalias foo bar baz`. The arguments `arg1 arg2 arg3 foo bar baz` would then be 
passed to the function assigned to the `myargs` command. 

The syntax to create/edit an alias is:
`alias add <alias name> <command>` 

The syntax to remove one or more aliases is:
`alias remove <alias name(s)>`

To view a list of all aliases, call the `alias` command with no arguments. This will show both the alias name as well as the
entire command that is assigned to it.

<!-- Note about alias names -->
> [!NOTE]
> Just like with command names, aliases can contain letters, numbers and symbols but
> not spaces. The reason is the same; it is because of how MagnetSting parses commands.

<!-- Command Help -->
## Command Help
The `help` command is used to show the main help banner, but it can also be used to show help for specific commands.
For example, if you call `help co`, a help banner consisting of all the commands and command groups that start with
`co` will be shown. Commands within command groups and aliases are not shown however. 

An additional form of help is the "possible commands" functionality. If you enter a command that does not exist, MagnetSting will
go through all of the commands and command group names and create a list of all of the ones that start with the first value in the
command (the command string is split into a list when it is parsed). MagnetSting will then pretty-print the possible commands in a 
tabular format. Commands within a command group will not show up, unless attempting to call a command within a command group, at
which point only the commands within the group will be checked. Aliases are also not included in the search.

<!-- Opening Banner -->
## Opening Banner
On start, MagnetSting will also display an opening banner along with the main help banner. You can use this banner to display 
anything you want. There are two ways to create a banner: using a tuple and letting MagnetSting create it for you or create your 
own custom banner. When using the first option, MagnetSting will just print the values of the tuple. The second option lets you 
have total control over how the banner looks. Using a custom banner is simple, just create it as a string object and then pass it 
to the `banner` parameter in the class initialization. 

Using a tuple:
```python
from magnetsting import MagnetSting

banner_tuple = ("="*25, "Hello, this is my opening banner", "="*25)

mast = MagnetSting(banner=banner_tuple)

mast.magnetsting_mainloop()
```

Using a string object (in this case, text read in from a file):
```python
from magnetsting import MagnetSting

with open("mybanner", "r") as banner_read:
    banner_str = banner_read.read()

mast = MagnetSting(banner=banner_str)

mast.magnetsting_mainloop()
```

<!-- Shell-like Behaviour -->
## Shell-like Behaviour
Because MagnetSting has the `readline` module imported, it automatically gains shell-like behaviour, allowing you to move
the input cursor back and forth using the left and right arrow keys and cycle through previously executed commands using 
the up and down arrow keys. You can also use the tab key to add a tab of spaces, though this will be replaced with 
command completion later on.

<!-- Branches -->
## Branches
The repository has two branches: `master` and `dev`. The `master` branch holds all the stable code and is updated once a new 
version is released. The `dev` branch on the other hand is updated more often, with all the new changes first being committed 
to `dev`. Once a new version of MagnetSting is ready, it is then merged with `master`. If you are planning on contributing
to MagnetSting, make sure to base your work off of the `dev` branch as it is always more up to date in terms of the latest
changes. 

<!-- License -->
## License
MagnetSting is licensed under the GNU GPLv3 license. The full license can be found in the `LICENSE` file.

<!-- Contributing -->
## Contributing
Interested in contributing to MagnetSting? Check out the `CONTRIBUTING.md` file, it holds all the information you need to
know to contrbiute to this project.

