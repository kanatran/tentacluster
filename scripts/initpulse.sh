# chown -R $USER:$USER $HOME/
test -f hasrun || {
    ulimit -n 10000
    touch hasrun

    apt install pulseaudio

    addgroup $USER audio
    addgroup $3 audio

    # apt install nautilus
    # nautilus &

    # https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/SystemWide/
    # systemctl --global disable pulseaudio.service pulseaudio.socket

    # https://superuser.com/questions/1223118/emulating-microphone-input-to-chrome-inside-docker-container

    # export DBUS_SESSION_BUS_ADDRESS=$(cat /proc/$(pidof nautilus | cut -f1 -d" ")/environ | tr '\0' '\n' | grep DBUS_SESSION_BUS_ADDRESS | cut -d '=' -f2-)

    echo "Load pulseaudio virtual audio source 1"
    # init pulseaudio server here

    # su -c "sh ./scripts/initpulse.sh $2" $1
    echo "sudo -u $3 sh ./scripts/run-runner.sh $2"
    sudo -u $3 ./scripts/run-runner.sh $2 $4 $5
    echo "Done with running script"
}