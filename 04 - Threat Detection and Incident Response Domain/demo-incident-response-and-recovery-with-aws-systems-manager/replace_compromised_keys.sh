#!/bin/bash

pub_key_string="%REPLACE_ME%"

file="/home/ec2-user/.ssh/authorized_keys"

# This completely overwrites the authorized key files!
# If you need to just append, use this command: sudo echo $pub_key_string >> $file
sudo echo $pub_key_string > $file
