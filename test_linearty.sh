#!/bin/bash
echo "Downloading the acc data: "
sudo python isensitgw_get_angle.py

echo "Test sensor linearty: "
sudo python SensorLinearty.py

