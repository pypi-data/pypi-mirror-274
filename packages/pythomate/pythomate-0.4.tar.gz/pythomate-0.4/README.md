# Pythomate

Pacote [pythomate](https://pypi.org/project/pythomate/) inicia fluxo(s) e rotina(s) de ferramentas Microsoft (como Power Automate e Power Bi)[^1] via linha de comando.
Aliado ao agendador de tarefas Windows cria-se gatilho(s)[^2].

## Instalação

O `pythomate` está disponível no Python Package Index - [PyPI](https://pypi.org/project/pythomate/), sendo **compatível apenas com sistema operacional Windows**.
Ele pode ser instalado utilizando-se o comando[^3]:

```bash
# Sugerimos a instalação em ambiente virtual
$ pip install pythomate
```

- Necessário adicionar ao `PATH` do Windows caminho de instalação das ferramentas Microsoft desejadas[^4].
- Para o Power Automate é necessário **desmarcar** a opção de configuração "Ao fechar, manter aplicativo em execução". Isso evita conflito entre instâncias abertas e a execução que será gerada com auxílio do pacote.

## Uso

Diretamente na linha de comando:

```bash
# Substitua <ferramenta> pela ferramenta que se deseja acionar (automate ou bi).
# Substitua <nome> pelo nome do fluxo/processo que deseja iniciar.
$ pythomate run <ferramenta> <nome>
```

Para maiores informações, consulte documentação disponível no próprio CLI, via `pythomate --help`.

## Contribuições

Veja o arquivo [`CONTRIBUTING.md`](CONTRIBUTING.md) para mais detalhes.

## Licença

O **pythomete** é licenciado sob a licença MIT.
Veja o arquivo [`LICENSE.txt`](LICENSE.txt) para mais detalhes.

Teste push.

[^1]: Atualmente encontra-se implantado apenas processos para Power Automate.
[^2]: Gatilhos que, em geral, não são permitidos em versões gratúitas destas ferramentas.
[^3]: Sugerimos a utilização da Git Bash disponível na instalação do programa [Git for Windows](https://gitforwindows.org/).
[^4]: Como exemplo, sabemos que a ferramenta Power Automate, em geral, encontra-se instalada em `C:/Program Files (x86)/Power Automate Desktop/`.
