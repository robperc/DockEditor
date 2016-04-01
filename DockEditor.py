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
		self.tiles       = ('file-tile', 'directory-tile', 'url-tile')
		self.id          = "com.apple.dock"
		self.apps        = NSMutableArray.alloc().initWithArray_(CoreFoundation.CFPreferencesCopyAppValue("persistent-apps", self.id))
		self.others      = NSMutableArray.alloc().initWithArray_(CoreFoundation.CFPreferencesCopyAppValue("persistent-others", self.id))
		self.labels      = self.getLabels()

	def getLabels(self):
		file_labels = [dock_item['tile-data']['file-label'] for dock_item in (self.apps + self.others) if dock_item['tile-data'].get('file-label') is not None]
		url_labels  = [dock_item['tile-data']['label'] for dock_item in (self.apps + self.others) if dock_item['tile-data'].get('label') is not None]
		return file_labels + url_labels

	def addApp(self, label, index=-1, section="apps"):
		label = label.split(".app")[0]
		try_paths = [path + label + '.app' for path in self.app_dirs]
		add_path = [path for path in try_paths if os.path.exists(path)]
		if not add_path:
			print "Can't find app: %s" % (label)
			return
		else:
			add_path = add_path[0]
		self.add(label, add_path, index=index, section=section)

	def addFile(self, uri, label=None, index=-1, section="apps"):
		if not os.path.isfile(uri):
			return
		if label == None:
			label = os.path.basename(uri)
		self.add(label, uri, index=index, section=section)

	def addDir(self, uri, label=None, index=-1, section="apps"):
		if not os.path.isdir(uri):
			return
		if label == None:
			label = os.path.basename(uri)
		self.add(label, uri, index=index, section=section, tile_type="directory-tile")

	def addUrl(self, label, url, index=-1):
		self.add(label, url, index=index, section="others", tile_type="url-tile")

	def add(self, label, uri, index=-1, section="apps", tile_type="file-tile"):

		if section == "apps":
			target = self.apps
		elif section == "others":
			target = self.others
		else:
			return

		if label in self.labels:
			return

		if tile_type not in self.tiles:
			return

		if index == -1 or index > len(target):
			index = len(target)
		elif index < -1:
			index = 0

		new_item = {
			'GUID': str(uuid.uuid4()).upper(),
			'tile-type': tile_type
		}

		if tile_type in ('file-tile', 'directory-tile'):
			if tile_type == 'file-tile':
				file_type = 32
			if tile_type == 'directory-tile':
				file_type = 2
			new_item['tile-data'] = {
				'file-data': {
					'_CFURLString': uri, 
					'_CFURLStringType': 0
				},
				'file-label': label,
				'file-type': file_type
			}
		else:
			new_item['tile-data'] = {
				'url': {
					'_CFURLString': uri, 
					'_CFURLStringType': 15
				},
				'label': label
			}

		target.insert(index, new_item)
		self.labels.append(label)

	def remove(self, label):
		for target in (self.apps, self.others):
			for dock_item in reversed(target):
				if dock_item['tile-data'].get('file-label') == label or dock_item['tile-data'].get('label'):
					self.labels.remove(label)
					target.remove(dock_item)
					return

	def removeAll(self, section="apps"):
		if section == "apps":
			target = self.apps
		elif section == "others":
			target = self.others
		else:
			return
		for item in target:
			info = item['tile-data']
			try:
				label = info['file-label'] if info.get('file-label') is not None else info['label']
				self.labels.remove(label)
			except:
				pass
		target[:] = []

	def move(self, label, index, section="apps"):
		if section == "apps":
			target = self.apps
		elif section == "others":
			target = self.others
		else:
			return
		if label not in self.labels:
			return
		if index == -1 or index > len(target):
			index = len(target)
		elif index < -1:
			index = 0
		for child in target:
			try:
				found = info['file-label'] if info.get('file-label') is not None else info['label']
			except:
				continue
			if found == label:
				to_mv = child
				break
		target.remove(to_mv)
		target.insert(index, to_mv)

	def swap(self, label1, label2):
		pass

	def write(self):
		CoreFoundation.CFPreferencesSetAppValue("persistent-apps", self.apps,  self.id)
		CoreFoundation.CFPreferencesSetAppValue("persistent-others", self.others,  self.id)
		CoreFoundation.CFPreferencesAppSynchronize(self.id)

