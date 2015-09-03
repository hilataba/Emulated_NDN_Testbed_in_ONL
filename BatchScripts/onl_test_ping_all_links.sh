#!/bin/bash

source ~/.topology

# CAIDA test links to UCLA, UCI, UA
ssh $h5x1 "ping -c 1 -q h11x1; ping -c 1 -q h7x1 ; ping -c 1 -q h3x1"
