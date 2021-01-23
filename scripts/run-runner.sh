#!/bin/bash
echo "Is running the thing"
sudo pulseaudio -vvvv -D
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

# Used for debugging audio
# echo Soundcards:
# pacmd list soundcards
# echo Sinks:
# pacmd list-sinks
# echo Sources:
# pacmd list-sources && echo listed sources


function bruhpv() {
	local bruh=""
	local newbruh=""
	while true
	do
		newbruh=$(cat bruh.txt)
		if [ "$newbruh" != "$bruh" ]
		then
			echo Playing $newbruh
			pkill mpv
			mpv --no-video $newbruh &
		fi
		bruh=$newbruh
		sleep 10
	done
}

touch bruh.txt
bruhpv &

echo Printing release
youtube-dl --version

pushd ..
git clone https://github.com/Botrans/baquap
pushd baquap
git config --global user.name 'Kanatran'
git config --global user.email '<>'
git remote set-url origin https://x-access-token:$3@github.com/kanatran/baquap.git
popd
popd

echo Machine $1

# Actual python should be at /opt/hostedtoolcache/Python/3.8.7/x64/bin/python3
echo Using $2
echo Action index $4
export CHANNEL_ID=$(jq .[$(($1 + $4))].channel channels.json | sed 's/"//g')
echo CHANNEL_ID: $CHANNEL_ID

if [ $CHANNEL_ID != "null" ]
then
	echo Using channel $CHANNEL_ID
	$2 -m pip install -r requirements.txt
	$2 -m pip install uvicorn fastapi
	$2 scripts/setup_chrome.py
	$2 -m uvicorn run_audio:app --app-dir=scripts --port=6969 &
	$2 -m uvicorn server:app --app-dir=scripts --port=42069
else
	echo Channel_ID was null, quiting
fi
