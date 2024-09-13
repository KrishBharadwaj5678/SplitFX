import streamlit as st
from moviepy.editor import *

st.set_page_config(
    page_title="SplitFX",
    page_icon="icon.png",
    menu_items={
        "About":"SplitFX provides a fast and intuitive way to combine videos into a split-screen layout. Whether for YouTube, Instagram, or any other platform, create professional-looking videos with just a few clicks."
    }
)

st.write("<h2 style='color:lightgreen;'>Combine Videos into Stunning Split Screens!</h2>",unsafe_allow_html=True)

file=st.file_uploader("Upload Videos",accept_multiple_files=True,type="mp4")
audio=st.radio("Keep Audio?",["Yes","No"])

clips=[]
# Fetching all videos
for i in range(0,len(file)):
    with open(f"video_{i}.mp4","wb") as vid:
        vid.write(file[i-1].getbuffer())

tduration=[]
for i in range(0,len(file)):
    tduration.append(VideoFileClip(f"video_{i}.mp4").duration)
min_dur=int(min(tduration)) if len(tduration)>=1 else None

start=st.slider("Start Time",min_value=1,max_value=min_dur)
end=st.slider("End Time",min_value=1,max_value=min_dur)

btn=st.button("Generate")
if btn:
     with st.spinner("Just a moment..."):
            if(end>start):
                count=0
                if(len(file)%2==0):
                    for i in range(0,2):
                        row=[]
                        for j in range(0,len(file)//2):
                            row.append(VideoFileClip(f"video_{count}.mp4").subclip(start,end) if audio=="Yes" else VideoFileClip(f"video_{count}.mp4").without_audio().subclip(start,end))
                            count+=1 
                        clips.append(row)
                    c=clips_array(clips)
                    c.write_videofile("split_screen.mp4")
                
                else:
                    row=[]
                    for j in range(0,len(file)):
                            tduration.append(VideoFileClip(f"video_{count}.mp4").duration)
                            row.append(VideoFileClip(f"video_{count}.mp4").subclip(0,10) if audio=="Yes" else VideoFileClip(f"video_{count}.mp4").without_audio().subclip(0,10))
                            count+=1 
                    clips.append(row)
                    c=clips_array(clips)
                    c.write_videofile("split_screen.mp4")

                st.video("split_screen.mp4")
                with open("split_screen.mp4","rb") as video:
                    st.download_button("Download",video.read(),"splitfx.mp4")
            else:
                st.error("Invalid Duration!")