#!/bin/bash
gnrdbsetup mybasket
echo "lanciate migrazioni"
gnrdaemon > /dev/null 2>&1 &
echo "avviato demone"
sleep 3
gnrwsgiserve mybasket
echo "avviato progetto"
