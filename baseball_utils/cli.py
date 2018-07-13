from datetime import datetime

import click

from baseball_utils.const import FieldingPos
from baseball_utils.gameday import GamedayData
from baseball_utils.get_today import Today
from baseball_utils.savant import Savant
from baseball_utils.util import SESSION


@click.command()
def cli():
    # click.echo('CLI')
    # td = Today(SESSION)
    click.secho(datetime.today().isoformat(), fg='black', bg='white')
    click.echo('')
    gd = GamedayData(SESSION, Savant(SESSION))
    for elem in gd.linescores():
        click.echo(str(elem))
        click.echo('')
    # for game in td.gd.master_scoreboard('game'):
    #     status = game.find('status')
    #     if status['ind'] == 'I':
    #         data_url = td.gd.gd_base + game['game_data_directory']
    #         inn_url = data_url + '/inning/inning_all.xml'
    #         print(inn_url)
    #         r = SESSION.head(inn_url)
    #         print(r, r.headers)
    # click.echo(gd.master_scoreboard.prettify())
