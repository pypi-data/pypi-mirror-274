# SPDX-FileCopyrightText: 2024-present Jason W. DeGraw <jason.degraw@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause
from flask import Flask, request
import os
import subprocess

from .__about__ import __version__

__all__ = ["__version__", "create_app"]

def create_app(config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        ENERGYPLUS='energyplus'
    )

    app.config.from_prefixed_env()

    if config is not None:
        app.config.from_mapping(config)
    
    @app.route('/run', methods=['POST'])
    def run_route():
        # POST request
        idf = request.form.get('idf')
        epw = request.form.get('epw')
        run_dir = request.form.get('run_dir')
        with open(os.path.join(run_dir, 'output.txt'), 'w') as output:
            subprocess.run([app.config['ENERGYPLUS'], '-w', epw, idf], cwd=run_dir, stdout=output, stderr=subprocess.STDOUT)
        return run_dir
    
    @app.route('/in', methods=['POST'])
    def in_route():
        # POST request
        run_dir = request.form.get('run_dir')
        # Should check that in.idf and in.epw are actually there
        with open(os.path.join(run_dir, 'output.txt'), 'w') as output:
            subprocess.run(app.config['ENERGYPLUS'], cwd=run_dir, stdout=output, stderr=subprocess.STDOUT)
        return run_dir

    return app


