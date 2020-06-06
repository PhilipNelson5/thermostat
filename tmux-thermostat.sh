#!/usr/bin/env bash

tmux new-session -s thermostat -d '/home/pi/thermostat/thermostat.py; bash'
tmux split-window -h '/home/pi/thermostat/web_server.py; bash'
tmux new-window 'chromium-browser --start-fullscreen http://localhost:4000; bash'
tmux select-window -t 0
#tmux attach -t thermostat
