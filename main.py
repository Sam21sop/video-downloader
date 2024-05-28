from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pytube import YouTube, Playlist
from typing import Optional
import os

app = FastAPI()

class VideoRequest(BaseModel):
    url: str
    resolution: Optional[str] = '720p'


@app.post("/download/")
async def download_video(request: VideoRequest):
    try:
        yt = YouTube(request.url)
        stream = yt.streams.filter(res=request.resolution, file_extension='mp4').first()
        if not stream:
            return HTTPException(status_code=404, detail="Resolution not found")
        
        output_path = os.path.join("downloads", f"{yt.title}.mp4")
        stream.download(output_path=output_path)
        
        return {"message": "Video downloaded successfully", "path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



def get_stream(yt: YouTube, requested_resolution: str):
    resolutions = ['2160p', '1440p', '1080p', '720p', '480p', '360p', '240p', '144p']
    res_index = resolutions.index(requested_resolution) if requested_resolution in resolutions else 3  # Default to 720p
    for res in resolutions[res_index:]:
        stream = yt.streams.filter(res=res, file_extension='mp4').first()
        if stream:
            return stream
    return None


@app.post("/download_playlist/")
async def download_playlist(request: PlaylistRequest):
    try:
        playlist = Playlist(request.url)
        download_paths = []
        for video_url in playlist.video_urls:
            yt = YouTube(video_url)
            stream = get_stream(yt, request.resolution)
            if not stream:
                return HTTPException(status_code=404, detail="No suitable resolution found for one or more videos")
            
            output_path = os.path.join("downloads", f"{yt.title}.mp4")
            stream.download(output_path=output_path)
            download_paths.append(output_path)
        
        return {"message": "Playlist downloaded successfully", "paths": download_paths}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def read_root():
    return {"message": "Welcome to the YouTube Video Downloader API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
