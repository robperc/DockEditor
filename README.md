# DockEditor
Python module for easily adding, removing, and moving items on the Finder Dock in the context of the logged in user.
Work in Progress.

Example Usage:
```
#!/usr/bin/python

from DockEditor import Dock                              # Import the module

dock = Dock()                                            # Create a Dock instance to act on.

dock.addApp("Terminal")                                  # Add 'Terminal' application to Dock. Defaults to adding items to 'apps' section.
dock.addFile("/Users/Shared/SomeFile", section="others") # Add 'SomeFile' file item to Dock in 'others' section.
dock.addDir("/Users/Shared", label="SharedDir")          # Add 'SharedDir' directory item to Dock. Specifying a label overrides the auto-generated basename label.
dock.addUrl("Reddit", "https://reddit.com", index=0)     # Add url item for 'Reddit' to Dock. url items can only be added to 'others' section.
dock.remove("Calendar")                                  # Remove 'Calendar' application from Dock.
dock.remove("Reddit")                                    # Remove 'Reddit' url item from Dock.

dock.write()

```

## Notes

- url-tile type Dock items only supported in the "persistent-others" section of Dock ( right side of | ).
- Dock may need to be killed after modification for changes to appear. This can be scripted with the snippet below if needed.
```
subprocess.check_call(["killall", "Dock"])
```