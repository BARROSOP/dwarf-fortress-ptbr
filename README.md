# Dwarf Fortress em PortuguÃªs (PT-BR) â€” instalador

Instalador grÃ¡fico para **Dwarf Fortress 53.16 (Steam, Windows x64)**. Traduz a interface e os textos do jogo para portuguÃªs do Brasil (31.902 frases). NÃ£o altera o `Dwarf Fortress.exe` nem os saves; faz backup do que sobrescreve e tem botÃ£o **Desinstalar**.

## Usar
1. Baixe `Instalar-DwarfFortress-PTBR-v3.1.exe` em [Releases](../../releases).
2. Execute. Ele acha o jogo pela Steam (ou escolha a pasta) e instala.
3. Abra o jogo pela Steam normalmente.

VersÃ£o diferente de 53.16 Ã© recusada. O Windows pode avisar sobre "editor desconhecido": o .exe nÃ£o Ã© assinado.

## Como funciona
Usa o hook [dfint/df-steam-hook-rs](https://github.com/dfint/df-steam-hook-rs) (MIT) via [DFHack/dfhooks](https://github.com/DFHack/dfhooks) (MIT), que troca os textos em tempo de execuÃ§Ã£o. O instalador baixa da fonte oficial (`dfint.github.io/update-data`, conferido por SHA-256) a configuraÃ§Ã£o, os offsets, a tabela CP850 e a fonte com acentos.

## Sobre a traduÃ§Ã£o
O dicionÃ¡rio (`payload/dfint-data/dictionary.csv`, CP850) foi **traduzido do zero por IA (Gemini)**, sem copiar traduÃ§Ãµes de terceiros, com glossÃ¡rio fixo e validaÃ§Ã£o automÃ¡tica de `%s`, `%d`, `\n`, espaÃ§os e codificaÃ§Ã£o. 569 entradas ficaram em inglÃªs de propÃ³sito (nomes e cÃ³digos). Pode haver erros: abra uma issue ou PR.

## Gerar o .exe
```
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name Instalar-DwarfFortress-PTBR-v3 --add-data "payload;payload" instalador.py
```

## LicenÃ§a
MIT (cÃ³digo e dicionÃ¡rio). Dwarf Fortress Ã© de Bay12 Games; projeto nÃ£o oficial e sem vÃ­nculo. DLLs do hook: MIT, licenÃ§as em `payload/licencas`.

