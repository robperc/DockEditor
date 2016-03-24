# DockEditor
Python module for easily adding, removing, and moving items on the Finder Dock in the context of the logged in user.
Work in Progress.

Example Usage:
```
#!/usr/bin/python

from DockEditor import Dock          # Import the module

dock = Dock()                        # Create a Dock instance to act on.

dock.remove("Calendar")              # Remove 'Calendar' application from Dock
dock.remove("Messages")              # Remove 'Messages' application from Dock
dock.add("Terminal")                 # Add 'Terminal' application to Dock

dock.write()

```

## Notes

- url-tile type Dock items only supported in the "persistent-others" section of Dock ( right side of | ).
- Dock may need to be killed after modification for changes to appear. This can be scripted with the snippet below if needed.
```
subprocess.check_call(["killall", "Dock"])
```
