# SPDX-FileCopyrightText: 2024-present Jason W. DeGraw <jason.degraw@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause
import httpx
import os
import time

script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)

idf_file = os.path.join(script_dir, '..', 'resources', '5ZoneAirCooled.idf') 
epw_file = os.path.join(script_dir, '..', 'resources', 'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw')
run_base_dir = os.path.join(script_dir, '..', 'run') # this one exists
run_dir = os.path.join(run_base_dir, '1')
os.mkdir(run_dir)

inputs = {'idf': idf_file, 'epw': epw_file, 'run_dir': run_dir}

start = time.time()
r = httpx.post('http://127.0.0.1:5000/run', data=inputs, timeout=None)
delta = time.time() - start

print('Done! (%s seconds)' % delta)
print(r.status_code, r.text)