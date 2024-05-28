from pytube import Playlist
pl = Playlist(input('Enter play list link: '))
print(f'Downloading...{pl.title}')
for vid in pl.videos:
  print(f'Downloading...')
  vid.streams.get_by_resolution('720p').download()
  print(f'Download Successfully')

print('Play List Download Successfully')

