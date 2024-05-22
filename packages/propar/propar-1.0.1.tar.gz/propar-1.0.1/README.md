# Donations
It takes me a long time to make these libraries. If you would like to support my work, Then you can follow my patreon :)

https://www.patreon.com/Schkimansky

# Library
This is a easy to use python library that allows you to convert units of measurement to others. 
For example, You can use the "time" function to convert seconds to minutes. 
```python
import conversa
result = conversa.time(90,  From="seconds",  To="minutes") # Output will be 1.5 minutes (1.5 as a integer)
print(result)
```

# Installation
```bash
pip install conversa
```

# Documentation
There are only 2 functions:
```python
run_command(command: str, timeout=None, get_both_output_and_errors=False, get_return_code=False)
run_commands(commands_array: list[str], timeout=None, get_both_output_and_errors=False, get_return_code=False)
```

Run_command takes a command as a string and then runs it. The return value of the function depends on the parameters.
For example, In this case the return value will be the text that you get when you run the command manually in the terminal.
```python
result = run_command("mkdir NewFolder") # If this command gets a error, it will return the error. However if theres no error, Then it will just return the text you get when you execute that command manually.
```

However, you can put a timeout parameter to stop the function once it takes too long (defined in seconds)

Also, theres the run_commands function.
Its the same as run_command but this time it runs multiple commands.

Thats pretty much all, This can be used as a alternative to CMake. And is more powerfull, easier, extensible, simpler, reliable
