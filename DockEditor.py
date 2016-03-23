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
		self.tiles       = ('file', 'directory', 'url')
		self.id          = "com.apple.dock"
		self.apps        = NSMutableArray.alloc().initWithArray_(CoreFoundation.CFPreferencesCopyAppValue("persistent-apps", self.id))
		self.others      = NSMutableArray.alloc().initWithArray_(CoreFoundation.CFPreferencesCopyAppValue("persistent-others", self.id))
		self.labels      = [dock_item['tile-data'].get('file-label') for dock_item in (self.apps + self.others) if dock_item['tile-data'].get('file-label') is not None]

	def add(self, label, index=-1, section="apps"):
		label = label.split(".app")[0]
		try_paths = [path + label + '.app' for path in self.app_dirs]
		add_path = [path for path in try_paths if os.path.exists(path)]

		if section == "apps":
			target = self.apps
		elif section == "others":
			target = self.others
		else:
			return

		if label in self.labels:
			return

		if not add_path:
			print "Can't find app: %s" % (label)
			return
		else:
			add_path = add_path[0]

		if index == -1 or index > len(target):
			index = len(target)
		elif index < -1:
			index = 0

		new_item = {
			'GUID': str(uuid.uuid4()).upper(), 
			'tile-data': {
				'file-data': {
					'_CFURLString': add_path, 
					'_CFURLStringType': 0
				},
				'file-label': label,
				'file-type': 32
			}, 
			'tile-type': 'file-tile'
		}
		target.insert(index, new_item)
		self.labels.append(label)

	def remove(self, label):
		for target in (self.apps, self.others):
			for dock_item in reversed(target):
				if dock_item['tile-data'].get('file-label') == label:
					self.labels.remove(label)
					target.remove(dock_item)
					return

	def move(self, label, index):
		pass

	def swap(self, label1, label2):
		pass

	def write(self):
		CoreFoundation.CFPreferencesSetAppValue("persistent-apps", self.apps,  self.id)
		CoreFoundation.CFPreferencesSetAppValue("persistent-others", self.others,  self.id)
		CoreFoundation.CFPreferencesAppSynchronize(self.id)

