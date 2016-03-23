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
		self.id          = "com.apple.dock"
		self.apps        = NSMutableArray.alloc().initWithArray_(CoreFoundation.CFPreferencesCopyAppValue("persistent-apps", self.id))
		self.others      = NSMutableArray.alloc().initWithArray_(CoreFoundation.CFPreferencesCopyAppValue("persistent-others", self.id))
		self.labels      = [dock_item['tile-data'].get('file-label') for dock_item in (self.apps + self.others) if dock_item['tile-data'].get('file-label') is not None]
		self.identifiers = [dock_item['tile-data'].get('bundle-identifier') for dock_item in (self.apps + self.others) if dock_item['tile-data'].get('bundle-identifier') is not None]

	def add(self, add_name, index=-1):
		try_paths = [path + add_name + '.app' for path in self.app_dirs]
		add_path = [path for path in try_paths if os.path.exists(path)]

		if not add_path:
			print "Can't find app: %s" % (add_name)
			return False
		else:
			add_path = add_path[0]

		# if item already in dock do not add
		for dock_item in self.apps:
			if dock_item['tile-data'].get('file-label') == add_name:
				print "item %s already found" % (add_name)
				return False

		label_name = add_name.split(".app")[0]

		new_item = {
			'GUID': str(uuid.uuid4()).upper(), 
			'tile-data': {
				'file-data': {
					'_CFURLString': add_path, 
					'_CFURLStringType': 0
				},
				'file-label': label_name, 
				'file-type': 32
			}, 
			'tile-type': 'file-tile'
		}
		self.apps.append(new_item)
		return True

	def remove(self, label):
		for dock_item in reversed(self.apps):
			if dock_item['tile-data'].get('file-label') == label:
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

