#!/bin/bash

sudo journalctl --flush --rotate

sudo journalctl --vacuum-time=1s
