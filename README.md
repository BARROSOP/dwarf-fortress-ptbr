# Dwarf Fortress em Português (PT-BR) — instalador

Instalador gráfico para **Dwarf Fortress 53.16 (Steam, Windows x64)**. Traduz a interface e os textos do jogo para português do Brasil (31.902 frases). Não altera o `Dwarf Fortress.exe` nem os saves; faz backup do que sobrescreve e tem botão **Desinstalar**.

## Usar
1. Baixe `Instalar-DwarfFortress-PTBR-v3.exe` em [Releases](../../releases).
2. Execute. Ele acha o jogo pela Steam (ou escolha a pasta) e instala.
3. Abra o jogo pela Steam normalmente.

Versão diferente de 53.16 é recusada. O Windows pode avisar sobre "editor desconhecido": o .exe não é assinado.

## Como funciona
Usa o hook [dfint/df-steam-hook-rs](https://github.com/dfint/df-steam-hook-rs) (MIT) via [DFHack/dfhooks](https://github.com/DFHack/dfhooks) (MIT), que troca os textos em tempo de execução. O instalador baixa da fonte oficial (`dfint.github.io/update-data`, conferido por SHA-256) a configuração, os offsets, a tabela CP850 e a fonte com acentos.

## Sobre a tradução
O dicionário (`payload/dfint-data/dictionary.csv`, CP850) foi **traduzido do zero por IA (Gemini)**, sem copiar traduções de terceiros, com glossário fixo e validação automática de `%s`, `%d`, `\n`, espaços e codificação. 569 entradas ficaram em inglês de propósito (nomes e códigos). Pode haver erros: abra uma issue ou PR.

## Gerar o .exe
```
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name Instalar-DwarfFortress-PTBR-v3 --add-data "payload;payload" instalador.py
```

## Licença
MIT (código e dicionário). Dwarf Fortress é de Bay12 Games; projeto não oficial e sem vínculo. DLLs do hook: MIT, licenças em `payload/licencas`.
