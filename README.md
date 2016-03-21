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

- Currently only supports addition of "file-tile" type items to Apps portion (left side of | ) of Dock.
