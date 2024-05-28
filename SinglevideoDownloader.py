from pytube import YouTube

#take link from user
link = YouTube(input('Enter Link : '))

print("Downloading...")

#link.streams.get_by_resolution('360p').download()
link.streams.get_by_resolution('720p').download()
#link.streams.get_by_resolution('480p').download()

print('Download Sucessfully')
