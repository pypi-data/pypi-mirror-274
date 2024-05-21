# SPDX-FileCopyrightText: 2024-present Jason W. DeGraw <jason.degraw@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause
import click
import energyplus_service as eps

from ..__about__ import __version__


@click.command()
@click.option('-e', '--energyplus', show_default=True, default='energyplus', help='energyplus executable to use.')
def dev(energyplus):
    """
    Run the dev app.
    """
    config = {
        'ENERGYPLUS': energyplus
    }
    app = eps.create_app(config=config)
    app.run(host='127.0.0.1', port=5000, debug=True)

@click.group(context_settings={'help_option_names': ['-h', '--help']}, invoke_without_command=False)
@click.version_option(version=__version__, prog_name='energyplus-service')
@click.pass_context
def energyplus_service(ctx: click.Context):
    pass

energyplus_service.add_command(dev)
