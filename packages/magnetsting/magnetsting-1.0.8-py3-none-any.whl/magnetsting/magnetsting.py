"""
**MAGNETSTING**\n
v1.0.8\n
Create command-line projects with ease.\n
`Copyright (C) 2024 darkmattergit`\n
-----------------------------------\n
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.\n

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.\n

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import subprocess
import readline
import json


class MagnetSting:
    """
    `MagnetSting` is a framework that simplifies the creation of command-line projects. It comes with many
    capabilities built into it, such as help banner creation, command suggestions, command aliasing and more.
    The framework allows you to create three types of commands: `single`, `args` and `file`.\n
    - `single`-type commands are commands that consist only of the command name. Anything typed after the command name
      will not be passed onto the function assigned to the command.
    - `args`-type commands allow for the use of arguments. Anything typed after the command name is passed to the
      function assigned to the command. For example, if the command name is `"foo"`, then you can call it by adding an
      argument (in this case "bar") to the command: `"foo bar"`. This would then pass `"bar"` to the function
      associated with the command `"foo"`.
    - `file`-type commands, rather than executing functions associated to command names like `single-` and `args-type`
      commands, instead executes Python files associated with the command name. This command is more geared towards
      files that can take arguments in the command-line, such as those that use the "argparse" or "click" modules,
      but there is no restriction that would prohibit one from assigning a Python file that does not take arguments.
      Arguments can be passed by typing them after the command name, just like with `args-type` commands. For example,
      assume that the command name "mycommand" has the file "myfile.py" assigned to it. Assuming it was created using
      the "argparse" module, you could call the help banner by typing "mycommand - -help". A file assigned to a
      file-type command does not need to be in the same project directory, it can be anywhere on a system. If the file
      is located somewhere other than the project directory, make sure to add the full or relative path to it.
    - Additionally, commands can be grouped together using `command groups`. Command groups are, as the name suggests,
      a way to organize commands into a specific group. Commands assigned to a command group do not show up in the
      help banner, rather, the command group name does instead. To view all commands within a group, call the command
      group's name. The syntax to call a command within a command group is `<command group name> <command name>
      <args (if args- or file-type command)>`.
    **NOTE:**\n
    Functions used by the `single`- and `args-type` commands **MUST** be created in a specific way inorder for
    `MagnetSting` to execute them.\n
    - `single-type`: The functions for `single-type` commands **MUST** have the following parameter:
      `additional_data: tuple`. The function cannot have any other parameters. The `additional_data` parameter allows
      you to pass other data such as strings, ints, objects, etc. to the function through a tuple.
    - `args-type`: The functions for `args-type` commands **MUST** have the following parameters:
      `command_args: list` **AND** `additional_data: tuple`. The function cannot have any other parameters. The
      `command_args` parameter is for the argument(s) used with the command (recall from the `args-type` example above,
      this would be "bar"), while the `additional_data` parameter allows you to pass other data such as strings, ints,
      objects, etc. to the function using a tuple.
    **NOTE:**\n
    The order in which the commands and command groups are created determines the order in which they appear in the help
    banner. The same applies for commands in command groups.
    """
    def __init__(self, exit_description: str = "exit MAGNETSTING",
                 banner: tuple | str = ("=" * 35, "MAGNETSTING", "Data here", "=" * 35), cmd_prompt: str = ">> ",
                 exit_message: str = "[*] Exiting", break_keywords: tuple = ("q", "quit", "exit"),
                 alias_file: str = ".alias.json", verbose: bool = True, help_on_start: bool = True):
        """
        Initialize instance of MagnetSting.
        :param exit_description: The description of the exit command.
        :param banner: A `tuple` of the information that will appear in the banner. This can include but is
                       not limited to: name, version number, etc. If you want to use a custom banner rather than the
                       one that the class creates using the tuple, use a `string` instead.
        :param cmd_prompt: The `prompt` of the input.
        :param exit_message: The `message` that will be printed out upon exiting.
        :param break_keywords: A `tuple` of keywords used to exit.
        :param alias_file: A JSON file that holds `command aliases`.
        :param verbose: In the help banner, show command types next to the command descriptions. Having the parameter
                        set to `True` will show the command types while `False` will not.
        :param help_on_start: Show the help banner on start or not. Setting it to `True` will show the help banner on
                              start while setting it to `False` will not. Even when set to `False`, the help banner
                              and help functionality can still be called using the "help" command.
        """

        # Initialize dicts for commands, command groups and command aliases
        self._commands_info = {}
        self._groups_dict = {}
        self._alias_dict = {}
        self.exit_description = exit_description
        self.banner_data = banner
        self.cmd_prompt = cmd_prompt
        self.exit_message = exit_message
        self.break_keywords = break_keywords
        self.alias_file = alias_file
        self.verbose = verbose
        self.help_on_start = help_on_start

        # Check if file is a JSON file
        if self.alias_file[-5:] != ".json":
            raise ValueError("File is not a JSON file")
        else:
            pass

    def _help_command(self) -> None:
        """
        Print the help banner.
        :return: None
        """
        # Calculate the amount of spacing needed between the commands and their help descriptions
        spacing = 0
        for commands in self._commands_info:
            if len(commands) > spacing:
                spacing = len(commands)
            else:
                pass

        # Add additional spacing to the len of the longest command name to make the columns more distinct and readable
        spacing += 5

        # Print commands and their help descriptions
        if self.verbose is False:
            print()
            print(f"  {'Command':{spacing}} {'Description'}")
            print(f"  {'-------':{spacing}} {'-----------'}")
            for commands in self._commands_info:
                print(f"  {commands:{spacing}} {self._commands_info[commands]['help']}")
            print()

        # Print commands, their help descriptions and the commands types
        else:
            # Calculate the amount of spacing needed between the command help descriptions and the types
            type_spacing = 0
            for command_types in self._commands_info:
                if len(self._commands_info[command_types]["help"]) > type_spacing:
                    type_spacing = len(self._commands_info[command_types]["help"])
                else:
                    pass

            # Add additional spacing to the len of the longest command description to make the columns more distinct
            # and readable
            type_spacing += 5

            print()
            print(f"  {'Command':{spacing}} {'Description':{type_spacing}} {'Type'}")
            print(f"  {'-------':{spacing}} {'-----------':{type_spacing}} {'----'}")

            for commands in self._commands_info:
                print(f"  {commands:{spacing}} {self._commands_info[commands]['help']:{type_spacing}} "
                      f"{self._commands_info[commands]['type']}")
            print()

    def _specific_commands_help(self, command_name: str = None) -> None:
        """
        Print a help banner containing specific commands.
        :param command_name: The name or partial name of the command(s) to look for.
        :return: None
        """
        # Initialize dict to hold command names and their descriptions
        command_help_dict = {}
        # Initialize ints for calculating spacing
        command_spacer = 0
        type_spacer = 0

        for commands in self._commands_info:
            if commands.startswith(command_name):
                command_help_dict[commands] = self._commands_info[commands]["help"]

                # Calculate base spacing between commands names and descriptions
                if len(commands) > command_spacer:
                    command_spacer = len(commands)

                else:
                    pass

                # Calculate base spacing between command descriptions and types
                if len(self._commands_info[commands]['help']) > type_spacer:
                    type_spacer = len(self._commands_info[commands]['help'])

                else:
                    pass

            else:
                pass

        # Add additional spacing
        if command_spacer < 5:
            command_spacer += 12
        else:
            command_spacer += 5

        type_spacer += 5

        if len(command_help_dict) == 0:
            print("[!] No command(s) found\n")

        else:
            if self.verbose is False:
                print()
                print(f"  {'Command':{command_spacer}} Description")
                print(f"  {'-------':{command_spacer}} -----------")
                for command_help in command_help_dict:
                    print(f"  {command_help:{command_spacer}} {self._commands_info[command_help]['help']}")
                print()

            else:
                print()
                print(f"  {'Command':{command_spacer}} {'Description':{type_spacer}} {'Type'}")
                print(f"  {'-------':{command_spacer}} {'-----------':{type_spacer}} {'----'}")

                for commands in command_help_dict:
                    print(f"  {commands:{command_spacer}} {self._commands_info[commands]['help']:{type_spacer}} "
                          f"{self._commands_info[commands]['type']}")
                print()

    def _help_command_group(self, group_name: str = None) -> None:
        """
        Print a help banner for a specific command group.
        :param group_name: The name of the group.
        :return: None
        """
        # Calculate the amount of spacing needed between the commands and their help descriptions
        spacing = 0
        for commands in self._groups_dict[group_name]:
            if len(commands) > spacing:
                spacing = len(commands)
            else:
                pass

        # Add additional spacing to the len of the longest command name to make the columns more distinct and readable
        spacing += 5

        # Print commands and their help descriptions
        if self.verbose is False:
            print()
            print(f"  {'Command':{spacing}} {'Description'}")
            print(f"  {'-------':{spacing}} {'-----------'}")
            for commands in self._groups_dict[group_name]:
                print(f"  {commands:{spacing}} {self._groups_dict[group_name][commands]['help']}")
            print()

        # Print commands, their help descriptions and the commands types
        else:
            # Calculate the amount of spacing needed between the command help descriptions and the types
            type_spacing = 0
            for command_types in self._groups_dict[group_name]:
                if len(self._groups_dict[group_name][command_types]["help"]) > type_spacing:
                    type_spacing = len(self._groups_dict[group_name][command_types]["help"])
                else:
                    pass

            # Add additional spacing to the len of the longest command description to make the columns more distinct
            # and readable
            type_spacing += 5

            print()
            print(f"  {'Command':{spacing}} {'Description':{type_spacing}} {'Type'}")
            print(f"  {'-------':{spacing}} {'-----------':{type_spacing}} {'----'}")

            for commands in self._groups_dict[group_name]:
                print(f"  {commands:{spacing}} {self._groups_dict[group_name][commands]['help']:{type_spacing}} "
                      f"{self._groups_dict[group_name][commands]['type']}")
            print()

    def _possible_commands(self, command_name: str = None, command_group: str = None) -> None:
        """
        Pretty print possible command names that start with the user input should the input not be in the commands_info
        dict. The output is displayed in columns, similar to how it would look if using the GNU "column" tool.
        :param command_name: The input from the user.
        :param command_group: The name of the command group if checking commands in a group. If left as None, it will
                              look through the "self._commands_info" dict instead.
        :return: None
        """

        # Initialize list that will hold the commands that start with the user input
        if command_group is None:
            possible_commands_list = [commands for commands in self._commands_info if commands.startswith(command_name)]
        else:
            possible_commands_list = [commands for commands in self._groups_dict[command_group] if
                                      commands.startswith(command_name)]

        # No commands found
        if len(possible_commands_list) == 0 and command_group is None:
            print("[!] No possible command(s) found\n")

        # No commands found in specified command group
        elif len(possible_commands_list) == 0 and command_group is not None:
            print(f"[!] No possible command(s) found in group '{command_group}'\n")

        else:
            # Get the length of the longest command name
            block_spacers = 0
            for commands in possible_commands_list:
                if len(commands) > block_spacers:
                    block_spacers = len(commands)
                else:
                    pass

            # Add extra spacing to the length of the longest command to be able to better see the commands
            block_spacers += 12

            # Add blank padding if the number of commands in the list is not a multiple of 4
            if len(possible_commands_list) % 4 != 0:
                for _ in range(4 - (len(possible_commands_list) % 4)):
                    possible_commands_list.append("")
            else:
                pass

            # Create a list that holds lists of 4 commands each
            start_counter = 0
            end_counter = 4
            command_blocks = []
            for _ in range(len(possible_commands_list) // 4):
                command_blocks.append(possible_commands_list[start_counter:end_counter])
                start_counter += 4
                end_counter += 4

            # Pretty print possible commands in rows of 4
            print("possible command(s):")
            for blocks in command_blocks:
                print(f"{blocks[0]:{block_spacers}}{blocks[1]:{block_spacers}}{blocks[2]:{block_spacers}}"
                      f"{blocks[3]}")
            print()

    def _alias_command(self, alias_list: list = None) -> None:
        """
        Method to create and edit, remove and view command aliases
        :param alias_list: The user input split into a list
        :return: None
        """
        if len(alias_list) < 2:
            print("[*] Use 'alias add <alias name> <command>' to add/edit aliases or 'alias remove <alias name(s)>' to "
                  "remove aliases")
            spacer = 0
            for aliases in self._alias_dict:
                if len(aliases) > spacer:
                    spacer = len(aliases)

                else:
                    pass

            # Add different amount of additional spacing depending on the value of "spacer" to avoid misaligned columns
            if spacer <= 5:
                spacer += 12
            else:
                spacer += 5

            print()
            print(f"  {'Alias':{spacer}} Full Command")
            print(f"  {'-----':{spacer}} ------------")
            for commands in self._alias_dict:
                print(f"  {commands:{spacer}} {self._alias_dict[commands]}")
            print()

        else:
            # Add a command alias
            if alias_list[1] == "add" and len(alias_list) >= 4:

                if alias_list[2] in self._commands_info or alias_list[2] in self.break_keywords:
                    print(f"[!] Cannot create alias, '{alias_list[2]}' is already in use as a command name\n")

                elif alias_list[3] not in self._commands_info:
                    print(f"[!] Cannot create alias, the command '{alias_list[3]}' does not exist\n")

                elif alias_list[3] in self._groups_dict and alias_list[4] not in self._groups_dict[alias_list[3]]:
                    print(f"[!] Cannot create alias, '{alias_list[4]}' does not exist as a command in the group "
                          f"'{alias_list[3]}'\n")

                else:
                    command_str = " ".join(alias_list[3:])
                    self._alias_dict[alias_list[2]] = command_str
                    print(f"[+] Added alias '{alias_list[2]}'\n")

            # Remove a command alias
            elif alias_list[1] == "remove" and len(alias_list) >= 3:
                for to_del in alias_list[2:]:
                    try:
                        del (self._alias_dict[to_del])

                    except KeyError:
                        print(f"[!] Alias '{to_del}' does not exist")

                    else:
                        print(f"[-] Removed alias '{to_del}'")
                print()

            else:
                print("[*] Use 'alias add <alias name> <command>' to add/edit aliases or 'alias remove <alias name(s)>'"
                      " to remove aliases\n")

    def add_command_type_single(self, command_name: str = None, command_help: str = None, command_group: str = None,
                                command_function: object = None, additional_data: tuple = None) -> None:
        """
        Create a `single-type` command. A single-type command consists only of a command name that when called,
        executes the function assigned to it. Anything typed after the command name is not passed to the function
        assigned to the command. Functions used in single-type commands **MUST** have the following parameter:
        `additional_data: tuple`.
        :param command_name: The `name` of the command.
        :param command_help: A short `descriptor` about what the command does.
        :param command_group: The `group` the command belongs to. Can be left as None if it does not belong to any
                              group.
        :param command_function: The `function` assigned to the command.
        :param additional_data: `Additional data` that gets sent over to the command's function.
        :return: None
        """
        if command_group is None:
            self._commands_info[command_name.strip()] = {
                "type": "single",
                "function": command_function,
                "help": command_help,
                "additional": additional_data,
            }

        else:
            if command_group.strip() in self._groups_dict:
                self._groups_dict[command_group.strip()][command_name.strip()] = {
                    "type": "single",
                    "function": command_function,
                    "help": command_help,
                    "additional": additional_data,
                }

            else:
                raise NotImplementedError(f"Group '{command_group}' does not exist")

    def add_command_type_args(self, command_name: str = None, command_help: str = None, command_group: str = None,
                              command_function: object = None, additional_data: tuple = None) -> None:
        """
        Create an `args-type` command. An args-type command differs from a `single-type` command by being able to take
        arguments after the command name. For example, if the command name is `foo`, then you can do: "foo bar baz",
        with "bar baz" being the argument(s). There are no limits on how many arguments there can be, they can be as
        long and as many as you would like. If you do not provide an argument to an args-type command, a message will be
        printed telling you that some form of an argument is required. Functions used in args-type commands **MUST**
        have the following function parameters: `command_args: list` **AND** `additional_data: tuple`.
        :param command_name: The `name` of the command.
        :param command_help: A short `descriptor` about what the command does.
        :param command_group: The `group` the command belongs to. Can be left as None if it does not belong to any
                              group.
        :param command_function: The `function` assigned to the command.
        :param additional_data: 'Additional data' that gets sent over to the command's function.
        :return: None
        """
        if command_group is None:
            self._commands_info[command_name.strip()] = {
                "type": "args",
                "function": command_function,
                "help": command_help,
                "additional": additional_data,
            }

        else:
            if command_group.strip() in self._groups_dict:
                self._groups_dict[command_group.strip()][command_name.strip()] = {
                    "type": "args",
                    "function": command_function,
                    "help": command_help,
                    "additional": additional_data,
                }

            else:
                raise NotImplementedError(f"Group '{command_group}' does not exist")

    def add_command_type_file(self, command_name: str = None, command_help: str = None, command_group: str = None,
                              command_file: str = None) -> None:
        """
        Create a `file-type` command. A file-type command is different from the other commands. Rather than
        executing functions associated to command names like `single-` and `args-type` commands, instead executes
        Python files associated with the command name. This command is more geared towards files that can take arguments
        in the command-line, such as those that use the "argparse" or "click" modules, but there is no restriction that
        would prohibit one from assigning a Python file that does not take arguments. Arguments can be passed by typing
        them after the command name, just like with `args-type` commands. For example, assume that command name
        "mycommand" has the file "myfile.py" assigned to it. Assuming it was created using "argparse", you could call
        the help banner by typing "mycommand - -help". A file assigned to a file-type command does not need to be in
        the same project directory, it can be anywhere on a system. If the file is located somewhere other than the
        project directory, make sure to add the full or relative path to the name of the file when creating the command.
        :param command_name: The `name` of the command.
        :param command_help: A short `descriptor` about what the command does.
        :param command_group: The `group` the command belongs to. Can be left as None if it does not belong to any
                              group.
        :param command_file: The name and (if needed) the `full or relative path` of the file assigned to the command.
        :return: None
        """
        if command_group is None:
            self._commands_info[command_name.strip()] = {
                "type": "file",
                "file": command_file,
                "help": command_help,
            }

        else:
            if command_group.strip() in self._groups_dict:
                self._groups_dict[command_group.strip()][command_name.strip()] = {
                    "type": "file",
                    "file": command_file,
                    "help": command_help,
                }

            else:
                raise NotImplementedError(f"Group '{command_group}' does not exist")

    def add_command_group(self, group_name: str = None, group_help: str = None) -> None:
        """
        Create a `command group`. A command group is, as the name suggests, a group of commands. Groups can be used to
        organize commands and to keep the main help banner from becoming too long and overwhelming. Any command can be
        assigned to a command group and commands within a group can also be aliased. Commands assigned to a group do not
        show up in the main help banner, rather, only the command group is shown. To see all commands assigned to a
        group, enter the group name and a help banner containing only the commands in the group will be shown. The
        syntax to call a command in a command group is: <command group name> <command name>
        <args (if args- or file-type)>.
        :param group_name: The `name` of the group.
        :param group_help: A short `description` of the group.
        :return: None
        """
        # Add group to groups dict
        self._groups_dict[group_name.strip()] = {}
        # Add group info to commands dict
        self._commands_info[group_name.strip()] = {
            "type": "group",
            "help": group_help,
        }

    def magnetsting_mainloop(self) -> None:
        """
        This method handles all `MagnetSting` operations. Call this method once all the commands and command
        groups have been created.
        :return: None
        """
        # Add built-in commands to commands dict
        self._commands_info["alias"] = {
            "type": "built-in",
            "help": "add, remove and view aliases",
        }

        self._commands_info["clear"] = {
            "type": "built-in",
            "help": "clear the screen",
        }

        self._commands_info["help"] = {
            "type": "built-in",
            "help": "print this help banner",
        }

        self._commands_info[self.break_keywords[0]] = {
            "type": "built-in",
            "help": self.exit_description,
        }

        # Print custom banner
        if type(self.banner_data) is str:
            print(self.banner_data)

            # Print help banner on start if True
            if self.help_on_start is True:
                self._help_command()

            # Do not print help banner on start if False
            else:
                pass

        # Print values from tuple
        else:
            for data in self.banner_data:
                print(data)

            # Print help banner on start if True
            if self.help_on_start is True:
                self._help_command()

            # Do not print help banner on start if False
            else:
                pass

        try:
            # Open json file and load aliases into dict
            with open(self.alias_file, "r") as jr:
                json_alias = json.load(jr)
                self._alias_dict = json_alias

        except FileNotFoundError:
            # Do nothing if file does not exist, it will be created when MagnetSting exits
            pass

        while True:
            # Get user input, strip both leading and trailing whitespace
            usr_input = str(input(self.cmd_prompt)).strip()

            # Create list by splitting user input string
            split_command = usr_input.split(" ")

            # Check if first element is a break keyword
            if split_command[0] in self.break_keywords:
                # Write aliases to json file
                with open(self.alias_file, "w") as jw:
                    json.dump(self._alias_dict, jw)

                # Show exit message and break out of loop, exiting MagnetSting
                print(self.exit_message)
                break

            # Print help banner containing specific commands
            elif len(split_command) > 1 and split_command[0] == "help":
                self._specific_commands_help(command_name=split_command[1])

            # === Begin built-in commands functionality ===

            # Print help banner
            elif split_command[0] == "help":
                self._help_command()

            # Clear the command line
            elif split_command[0] == "clear":
                subprocess.run("clear", shell=True)

            # Call self._alias_command method to handle alias operations
            elif split_command[0] == "alias":
                self._alias_command(alias_list=split_command)

            # === End built-in commands functionality ===

            # Show commands in command group
            elif len(split_command) == 1 and split_command[0] in self._groups_dict:
                self._help_command_group(group_name=split_command[0])

            else:
                # Get the name of the command
                check_name = split_command[0]

                # Check if command exists as a name, group name or alias
                if check_name in self._commands_info or check_name in self._alias_dict or check_name in \
                        self._groups_dict:
                    # Initialize list to hold full command after determining if it is an alias or an actual command name
                    full_command_list = None

                    # Initialize dict to hold specific command info
                    command_dict = {}

                    # Check if command is a command name or a group name
                    if check_name in self._commands_info and self._commands_info[check_name]["type"] != "group":
                        # First element is not a group name
                        full_command_list = split_command

                        # Add command information from self._commands_info to command_dict
                        command_dict[check_name] = self._commands_info[check_name]

                    elif check_name in self._commands_info and self._commands_info[check_name]["type"] == "group":
                        try:
                            # First element is a group name, create list including everything except for the first
                            # element
                            full_command_list = split_command[1:]

                            # Add command information from self._commands_info to command_dict
                            command_dict[split_command[1]] = self._groups_dict[check_name][split_command[1]]

                        # Command does not exist in group, call self._possible_commands method to show possible commands
                        # user may have meant and continue to start
                        except KeyError:
                            self._possible_commands(command_name=split_command[1], command_group=check_name)
                            continue

                    # If first element is not a command or command group name, check if it is an alias
                    elif check_name in self._alias_dict:
                        alias_list = f"{self._alias_dict[check_name]} {' '.join(split_command[1:])}".split()

                        # Check if first element in alias_list actually exists as a command or command group
                        if alias_list[0] in self._commands_info:

                            # Check if name is a group name
                            if self._commands_info[alias_list[0]]["type"] == "group":

                                # Check if command exists in group, if it does, add information to dict and full command
                                # to list
                                if alias_list[1] in self._groups_dict[alias_list[0]]:
                                    command_dict[alias_list[1]] = self._groups_dict[alias_list[0]][alias_list[1]]
                                    full_command_list = alias_list[1:]

                                # Command does not exist in group, display message and continue to start
                                else:
                                    print(f"[!] Cannot execute alias '{check_name}', the command '{alias_list[1]}' "
                                          f"does not exist in the group '{alias_list[0]}'\n")
                                    continue

                            else:
                                full_command_list = (f"{self._alias_dict[check_name]} "
                                                     f"{' '.join(split_command[1:])}").split()
                                command_dict[alias_list[0]] = self._commands_info[alias_list[0]]

                        # First element of aliased command does not exist as a command or command group, display message
                        # and continue to start
                        else:
                            print(f"[!] Could not execute alias '{check_name}', the command or command group "
                                  f"'{alias_list[0]}' does not exist\n")
                            continue

                    # === Single Commands ===
                    if command_dict[full_command_list[0]]["type"] == "single":
                        # Call the function assigned to command, passing on any additional data specified with the
                        # command
                        command_dict[full_command_list[0]]["function"](additional_data=command_dict
                                                                       [full_command_list[0]]["additional"])

                    # === Args Commands ===
                    elif command_dict[full_command_list[0]]["type"] == "args":
                        # Check if there is at least one argument supplied after command name, display message if
                        # there is nothing
                        if len(full_command_list) == 1 or full_command_list[1].isspace() or full_command_list[1] == "":
                            print("[!] Argument required\n")

                        else:
                            # Create list of everything after command name
                            get_arg = full_command_list[1:]

                            # Call function assigned to command, passing on list of arguments and any additional data
                            # specified with the command
                            command_dict[full_command_list[0]]["function"](command_args=get_arg,
                                                                           additional_data=command_dict
                                                                           [full_command_list[0]]["additional"])

                    # === File Commands ===
                    elif command_dict[full_command_list[0]]["type"] == "file":
                        # Create string from the list sans the first element
                        parser_args = " ".join(full_command_list[1:])

                        # Execute file with (or without) arguments typed after command name
                        subprocess.run(f"python3 {command_dict[full_command_list[0]]['file']} {parser_args}",
                                       shell=True)

                    # === Aliased alias commands ===
                    elif full_command_list[0] == "alias":
                        self._alias_command(alias_list=full_command_list)

                else:
                    # If nothing was typed, do nothing
                    if usr_input == "" or usr_input.isspace():
                        pass

                    # If something was typed but nothing matched the first element, call self._possible_commands method
                    # to show possible commands the user may have meant, does not include commands in command groups or
                    # aliases
                    else:
                        self._possible_commands(command_name=check_name)
