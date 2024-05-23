import click
from .power_automate import run_power_automate_flow_cli


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.pass_context
@click.version_option()
def cli(ctx):
  """
    CLI para iniciar fluxo(s) e rotina(s) de ferramentas Microsoft (como Power Automate e Power Bi) via linha de comando.
    Aliado ao agendador de tarefas Windows cria-se gatilho(s) que, em geral, não são permitidos em versões gratúitas destas ferramentas.
  """

@cli.group()
def run():
  """
    Inicia fluxo(s) e rotina(s) de ferramentas Microsoft (como Power Automate e Power Bi).
  """

run.add_command(run_power_automate_flow_cli)
