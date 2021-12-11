#!/bin/bash
echo "--------- starting server"
python Game_Server.py &
pid1=$(echo "$!")
echo "--------- starting client 1"
python Game_Client.py name1 &
pid2=$(echo "$!")
echo "--------- starting client 2"
python Game_Client.py name2 &
pid3=$(echo "$!")
echo "hit ENTER to terminate"
read my_var
echo "stopping clients and server"
kill -9 $pid2 $pid3
sleep 0.1
kill -9 $pid1
