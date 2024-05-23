# Pythomate

Pacote [pythomate](https://pypi.org/project/pythomate/) inicia fluxo(s) e rotina(s) de ferramentas Microsoft (como Power Automate e Power Bi) via linha de comando.
Aliado ao agendador de tarefas Windows cria-se gatilho(s)[^1].

## Instalação

O `pythomate` está disponível no Python Package Index - [PyPI](https://pypi.org/project/pythomate/), sendo **compatível apenas com sistema operacional Windows**.
Ele pode ser instalado utilizando-se o comando[^2]:

```bash
# Sugerimos a instalação em ambiente virtual
$ pip install pythomate
```

Necessário adicionar ao `PATH` do Windows caminho de instalação das ferramentas Microsoft desejadas[^3].

## Uso

Diretamente na linha de comando:

```bash
# Substitua <ferramenta> pela ferramenta que se deseja acionar (automate ou bi).
# Substitua <nome-fluxo> pelo nome do fluxo que deseja iniciar.
$ pythomate run <ferramenta> <nome-fluxo>
```

Para maiores informações, consulte documentação disponível no próprio CLI, via `pythomate --help`.

## Contribuições

Veja o arquivo [`CONTRIBUTING.md`](CONTRIBUTING.md) para mais detalhes.

## Licença

O **pythomete** é licenciado sob a licença MIT.
Veja o arquivo [`LICENSE.txt`](LICENSE.txt) para mais detalhes.

Teste push.

[^1]: Gatilhos que, em geral, não são permitidos em versões gratúitas destas ferramentas.
[^2]: Sugerimos a utilização da Git Bash disponível na instalação do programa [Git for Windows](https://gitforwindows.org/). 
[^3]: Como exemplo, sabemos que a ferramenta Power Automate, em geral, encontra-se instalada em `C:/Program Files (x86)/Power Automate Desktop/`.
