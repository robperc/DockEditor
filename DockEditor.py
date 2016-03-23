import os
import uuid
import CoreFoundation
from Foundation import NSMutableArray


class Dock(object):

	def __init__(self):
		self.app_dirs = ('/Applications/', 
			'/Applications/Microsoft Office 2011/', 
			'/Applications/Utilities/', 
			'/System/Library/CoreServices/', 
			'/System/Library/CoreServices/Applications/'
		)
		self.sections    = ('persistent-apps', 'persistent-others')
		self.id          = "com.apple.dock"
		self.apps        = NSMutableArray.alloc().initWithArray_(CoreFoundation.CFPreferencesCopyAppValue("persistent-apps", self.id))
		self.others      = NSMutableArray.alloc().initWithArray_(CoreFoundation.CFPreferencesCopyAppValue("persistent-others", self.id))
		self.labels      = [dock_item['tile-data'].get('file-label') for dock_item in (self.apps + self.others) if dock_item['tile-data'].get('file-label') is not None]

	def addApp(self, app_name, index=-1):
		app_name = app_name.split(".app")[0]
		try_paths = [path + app_name + '.app' for path in self.app_dirs]
		add_path = [path for path in try_paths if os.path.exists(path)]

		if app_name in self.labels:
			return

		if not add_path:
			print "Can't find app: %s" % (app_name)
			return
		else:
			add_path = add_path[0]

		if index == -1 or index > len(self.apps):
			index = len(self.apps)
		elif index < -1:
			index = 0

		new_item = {
			'GUID': str(uuid.uuid4()).upper(), 
			'tile-data': {
				'file-data': {
					'_CFURLString': add_path, 
					'_CFURLStringType': 0
				},
				'file-label': app_name,
				'file-type': 32
			}, 
			'tile-type': 'file-tile'
		}
		self.apps.insert(index, new_item)
		self.labels.append(app_name)

	def remove(self, label):
		for dock_item in reversed(self.apps):
			if dock_item['tile-data'].get('file-label') == label:
				self.labels.remove(label)
				self.apps.remove(dock_item)
				return

	def move(self, label, index):
		pass

	def swap(self, label1, label2):
		pass

	def write(self):
		CoreFoundation.CFPreferencesSetAppValue("persistent-apps", self.apps,  self.id)
		CoreFoundation.CFPreferencesSetAppValue("persistent-others", self.others,  self.id)
		CoreFoundation.CFPreferencesAppSynchronize(self.id)

