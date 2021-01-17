#!/bin/bash
echo "Is running the thing"
pulseaudio -vvvv -D
echo "Have run the thing"
sleep 10

echo "Create virtual output device (used for audio playback)"
pactl load-module module-null-sink sink_name=DummyOutput sink_properties=device.description="CustomSpeaker"

echo 'Create virtual microphone output, used to play media into the "microphone"'
pactl load-module module-null-sink sink_name=CustomAudioPipe sink_properties=device.description="CustomMicrophone"

echo "Set the default source device (for future sources) to use the monitor of the virtual microphone output"
pacmd set-default-source CustomAudioPipe.monitor

echo "Create a virtual audio source linked up to the virtual microphone output"
pacmd load-module module-virtual-source source_name="CustomMicrophone"

echo Soundcards:
pacmd list soundcards
echo Sinks:
pacmd list-sinks
echo Sources:
pacmd list-sources && echo listed sources

function mplay() {
    echo Playing $1
    mpv --no-video $1 &> /dev/null
    echo Finished playing $1
    pkill uvicorn
    pkill chrome
    exit 0
}

# node runner/index.js $1 &
# cd dictation-kit
echo Printing release
youtube-dl --version
# live="https://www.youtube.com/watch?v="$(curl -s https://jetrico.sfo2.digitaloceanspaces.com/hololive/youtube.json | jq .live[$1].yt_video_key | sed 's/"//g')

# live="https://www.youtube.com/watch?v=fxhrQCIeSOQ"
echo Mashine $1
live=$(jq .[$1] links.json | sed 's/"//g')
mplay $live &

# Actual python should be at /opt/hostedtoolcache/Python/3.8.7/x64/bin/python3
echo Using $2
$2 -m pip install -r requirements.txt
$2 -m pip install uvicorn fastapi
$2 -m uvicorn server:app --app-dir=scripts --port=42069

# mpv --no-video $live &
# echo PCM devices available
# this works, used for testing
# arecord -L
# arecord -r 128000 -d 10 output.wav

# git clone https://github.com/julius-speech/dictation-kit
# pushd dictation-kit
# git lfs install
# # rm julius.dnnconf
# # cp ../julius.dnnconf julius.dnnconf
# # padsp 
# ./bin/linux/julius -C main.jconf -C am-gmm.jconf -input pulseaudio \
# -fallback1pass \
# -multipath \
# -quiet \
# -nostrip \
# -rejectshort 0 \
# -realtime \
# -forcedict &
# 
# sleep 10
# echo Transcribing $live 
# mplay $live
# 
# # sh run-linux-gmm.sh -input mic -nostrip
# popd