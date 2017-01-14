class Row:
	def __init__(self,track, artist, album, time):
		self.track = track
		self.artist = artist
		self.album = album
		self.time = time
		self.uri = 'NONE'
	def __str__(self):
		if self.album == ' ' or self.album == '' or self.album == u'\xa0' or self.album.find('78') != -1 or self.album.find('single') != -1 or self.album.find('Single') != -1:
			return 'track:' + self.track +  ' artist:' + self.artist + ' '
		else:
			return 'track:' + self.track +  ' artist:' + self.artist + ' album:' +self.album + ' '

	def set_uri(self,uri):
		self.uri = uri
