# Dwarf Fortress em Português (PT-BR)

Instalador gráfico da tradução para **Dwarf Fortress 53.16 (Steam, Windows x64)**. Traduz a interface e os textos do jogo para português do Brasil (31.902 frases).

- Não altera o `Dwarf Fortress.exe` nem os seus saves.
- Faz backup do que sobrescreve e tem o botão **Desinstalar**.

## Como instalar

1. Baixe `Instalar-DwarfFortress-PTBR-v3.1.exe` na página de [Releases](../../releases/latest).
2. Execute o arquivo. Ele acha o jogo pela Steam (ou você escolhe a pasta) e instala.
3. Abra o jogo pela Steam normalmente.

> **Aviso do Windows:** o `.exe` não é assinado, então o SmartScreen pode avisar de "editor desconhecido". Clique em *Mais informações → Executar assim mesmo*.
>
> Outra versão do jogo que não seja a 53.16 é recusada pelo instalador.

Se o download dos arquivos oficiais falhar (rede ou antivírus), o instalador tenta 3 espelhos. Como último recurso, coloque os 4 arquivos oficiais numa pasta `arquivos-oficiais` ao lado do `.exe`.

## Mande seu feedback

Esta é uma tradução feita por IA, então **vai ter erro**: termos estranhos, frases ruins e textos que vazam das caixas de menu. Ela melhora com o que você relatar.

**[Abra um feedback aqui](../../issues/new/choose)** e conte:

- onde viu o problema (tela ou menu);
- o que está escrito e como deveria ser;
- se possível, um print.

Eu reviso os relatos de tempos em tempos e publico versões atualizadas. Use **Watch → Releases** para ser avisado quando sair uma nova.

## Como funciona

Usa o hook [dfint/df-steam-hook-rs](https://github.com/dfint/df-steam-hook-rs) (MIT), carregado via [DFHack/dfhooks](https://github.com/DFHack/dfhooks) (MIT), que troca os textos em tempo de execução. O instalador baixa da fonte oficial (`dfint.github.io/update-data`, conferido por SHA-256) a configuração, os offsets, a tabela CP850 e a fonte com acentos.

## Sobre a tradução

O dicionário (`payload/dfint-data/dictionary.csv`, CP850) foi **traduzido do zero por IA (Gemini)**, sem copiar traduções de terceiros, com glossário fixo e validação automática de `%s`, `%d`, `\n`, espaços e codificação. 569 entradas ficaram em inglês de propósito (nomes e códigos).

## Gerar o .exe

```
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name Instalar-DwarfFortress-PTBR --add-data "payload;payload" instalador.py
```

## Licença

MIT (código e dicionário). Dwarf Fortress é de Bay12 Games; este projeto é não oficial e sem vínculo com eles. As DLLs do hook são MIT, com as licenças em `payload/licencas`.
