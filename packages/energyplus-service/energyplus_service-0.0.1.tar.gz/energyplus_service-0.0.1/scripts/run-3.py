# SPDX-FileCopyrightText: 2024-present Jason W. DeGraw <jason.degraw@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause
import os
import asyncio
import httpx
import shutil
import time

script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)

idf_dir = os.path.join(script_dir, '..', 'resources')
idf_files = ['5ZoneAirCooled.idf',
             '5ZoneCoolBeam.idf',
             'AirflowNetwork_MultiZone_SmallOffice.idf',
             'CoolingTower.idf',
             '1ZoneUncontrolled.idf',
             'AirCooledElectricChiller.idf']
epw_dir = os.path.join(script_dir, '..', 'resources')
epw_file = 'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw'

run_base_dir = os.path.join(script_dir, '..', 'run') # this one exists
run_dirs = [os.path.join(run_base_dir, '3%s'%el) for el in ['A', 'B', 'C', 'D', 'E', 'F']]
for run_dir, idf_file in zip(run_dirs, idf_files):
    os.mkdir(run_dir)
    shutil.copy(os.path.join(epw_dir, epw_file), os.path.join(run_dir, epw_file))
    shutil.copy(os.path.join(idf_dir, idf_file), os.path.join(run_dir, idf_file))

data = [{'idf': idf, 'epw': epw_file, 'run_dir': dir} for idf,dir in zip(idf_files, run_dirs)]

async def run():
    async with httpx.AsyncClient() as client:
        tasks = [client.post('http://127.0.0.1:5000/run', data=inputs, timeout=None) for inputs in data]
        result = await asyncio.gather(*tasks)
        return result

start = time.time()
result = asyncio.run(run())
delta = time.time() - start

print('Done! (%s seconds)' % delta)
for el in result:
    print(el.status_code, el.text)