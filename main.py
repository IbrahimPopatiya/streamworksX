from fastapi import FastAPI,UploadFile,File,HTTPException,BackgroundTasks,Depends
import shutil

from crud import extract_text_from_img,download_yt_video,download_yt_playlist,download_audio_from_video,download_audio_from_playlist
import uvicorn
import os
import re
from models import Files
from database import engine,SessionLocal,Base
from fastapi.responses import StreamingResponse,HTMLResponse,FileResponse
import schemas,models
from sqlalchemy.orm import Session
from sqlalchemy import text

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()      
                    



@app.post('/get_text')
async def img_text(Image:UploadFile = File(...)):
    accepted_file_types = ["image/png", "image/jpeg", "image/jpg", "image/heic", "image/heif", "image/heics", "png",
                          "jpeg", "jpg", "heic", "heif", "heics" 
    ] 
    if Image.content_type not in accepted_file_types:
        raise HTTPException(400, detail="Invalid document type")
    image_path = f"./data/{Image.filename}"
    with open(image_path,"wb") as buffer:
        buffer.write(await Image.read())
    response = extract_text_from_img(image_path)
    return response

@app.post('/download_yt_video',response_model=schemas.GetVideo)
def download_youtube_video(request: schemas.VideoURL, db:Session = Depends(get_db)):
        youtube_pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"
        playlist_pattern = r"[?&]list="
        url = str(request.url)
        
        if not re.match(youtube_pattern,url):
             raise HTTPException(status_code=400, detail="Invalid URL: Not a YouTube link")

        if re.search(playlist_pattern,url):
              raise HTTPException(status_code=400, detail="Please provide a video URL, not a playlist URL")

        
        video_uuid = download_yt_video(url,request.username,db)
    

        return {"video_uuid": str(video_uuid)}



@app.get('/get_video/{uuidname}')
def get_video(uuidname:str,db:Session = Depends(get_db)):
    # user = db.query(models.Video).filter(models.Video.id == id).first()
    query = text("SELECT * FROM files WHERE uuidname = :uuidname LIMIT 1")
    user = db.execute(query,{"uuidname": uuidname}).fetchone()
    print(query)
    print(uuidname)
    print(user)
    if not user:
          return {"error": "Video not found"}
    
    file_extension = user[5]
    print(file_extension)
    video_path = f"./data/{uuidname}.{file_extension}"

    if not os.path.exists(video_path):
        return{"error":"Video file not found"}
      
    return FileResponse(video_path,media_type="video/mpeg",filename=f"{uuidname}.{Files.filextension}")


@app.get("/get_user_files/{username}")
def get_files_from_user(username:str,db:Session = Depends(get_db)):
     query2 = text("SELECT * FROM files WHERE username = :username")
     result = db.execute(query2,{"username": username}).fetchall()   
     print(result)   
     downloads_list = [dict(row._mapping) for row in result]
     return downloads_list

@app.post("/get_yt_playlist")
def download_youtube_playlist(path:str):
    youtube_pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"
    if not re.match(youtube_pattern,path):
             raise HTTPException(status_code=400, detail="Invalid URL: Not a YouTube link")
    
    download_yt_playlist(path)
    return "playlist downloaded"

@app.post("/get_audio_of_video")
def download_audio_of_video(request: schemas.VideoURL,db:Session = Depends(get_db)):
    youtube_pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"
    playlist_pattern = r"[?&]list="

    url = str(request.url)

    if not re.match(youtube_pattern,url):
             raise HTTPException(status_code=400, detail="Invalid URL: Not a YouTube link")
    
    if re.search(playlist_pattern,url):
              raise HTTPException(status_code=400, detail="Please provide a video URL, not a playlist URL")
    

    audio_id = download_audio_from_video(url,db)



    return {"audio_id": str(audio_id)}


@app.get('/get_audio/{id}')
def get_audio(id:str,db:Session = Depends(get_db)):
    user = db.query(models.Audio).filter(models.Audio.id == id).first()
    audio_path = f"./videos/{user.filename}"


    if not user:
          return {"error": "Video not found"}

    if not os.path.exists(audio_path):
        return{"error":"Video file not found"}
      
    return FileResponse(audio_path,media_type="audio/mp4",filename=user.filename)


@app.post("/get_audio_of_playlist")
def download_audio_of_playlist(path:str):
    youtube_pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"
    if not re.match(youtube_pattern,path):
             raise HTTPException(status_code=400, detail="Invalid URL: Not a YouTube link")
    
    download_audio_from_playlist(path)
    return "audio playlist downloaded"



if __name__ == "__main__":
    uvicorn.run(
        app = app,
        host = "localhost",
        port = 3000
    )