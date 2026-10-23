"""Instalador PT-BR para Dwarf Fortress 53.16 Steam (hook dfint + dicionario)."""
import hashlib, json, os, re, shutil, struct, sys, time
from pathlib import Path

EXPECTED_TS = 0x6A70A6D9
BACKUP = "dfint-backup-ptbr"
LOG = "instalador-ptbr.json"


def payload_dir():
    return Path(getattr(sys, "_MEIPASS", Path(__file__).parent)) / "payload"


def pe_timestamp(exe):
    with open(exe, "rb") as f:
        d = f.read(4096)
    off = struct.unpack_from("<I", d, 0x3C)[0]
    if d[off:off + 4] != b"PE\0\0":
        raise ValueError("não é um executável PE")
    return struct.unpack_from("<I", d, off + 8)[0]


def steam_libraries():
    libs = []
    roots = []
    try:
        import winreg
        for hive, key, val in ((winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
                               (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath")):
            try:
                with winreg.OpenKey(hive, key) as k:
                    roots.append(Path(winreg.QueryValueEx(k, val)[0]))
            except OSError:
                pass
    except ImportError:
        pass
    for d in "CDEFGH":
        roots.append(Path(f"{d}:/Program Files (x86)/Steam"))
        roots.append(Path(f"{d}:/Steam"))
        roots.append(Path(f"{d}:/SteamLibrary"))
    for r in list(roots):
        vdf = r / "steamapps" / "libraryfolders.vdf"
        if vdf.exists():
            try:
                for m in re.finditer(r'"path"\s+"([^"]+)"', vdf.read_text(errors="ignore")):
                    libs.append(Path(m.group(1).replace("\\\\", "\\")))
            except OSError:
                pass
    libs += roots
    seen, out = set(), []
    for p in libs:
        k = str(p).lower()
        if k not in seen:
            seen.add(k)
            out.append(p)
    return out


def find_game():
    found = []
    for lib in steam_libraries():
        g = lib / "steamapps" / "common" / "Dwarf Fortress"
        if (g / "Dwarf Fortress.exe").exists():
            found.append(g)
    return found


BASE = "https://dfint.github.io/update-data/store/"
# baixados da fonte oficial (dfint/update-data) na hora da instalacao; conferidos por SHA-256
BAIXAR = {
    "dfint-data/config.toml": ("config.toml", "6c12a2c6b98835bea2b92466be1b2761af644e4ea8cf107b4358284e3a532359"),
    "dfint-data/offsets.toml": ("offsets/53.16_steam_win64.toml", "55293a6ede723dd7501c63049400752f4588466dfbdf6bfeb44ab5edc559df18"),
    "dfint-data/encoding.toml": ("encodings/cp850.toml", "9861daff639f67be75f15415e112c55121379ab6652db51a9b53a90157affd86"),
    "data/art/curses_640x300.png": ("fonts/cp850.png", "911f6fb011543ecdccfe57a2d2fa02261bb4dbce9d5c2fdef752c96b55a469dd"),
}


MIRRORS = [
    "https://dfint.github.io/update-data/store/",
    "https://raw.githubusercontent.com/dfint/update-data/main/store/",
    "https://cdn.jsdelivr.net/gh/dfint/update-data@main/store/",
]


def baixar(dst, cache, log=print):
    """Tenta cada espelho (3x cada); por fim usa arquivo local em 'arquivos-oficiais' ao lado do .exe."""
    import urllib.request
    rel, sha = BAIXAR[dst]
    nome = rel.split("/")[-1]
    erros = []
    for base in MIRRORS:
        for tent in range(3):
            try:
                req = urllib.request.Request(base + rel, headers={"User-Agent": "Mozilla/5.0 (DF-PTBR installer)"})
                data = urllib.request.urlopen(req, timeout=30).read()
                if hashlib.sha256(data).hexdigest() != sha:
                    raise RuntimeError("SHA-256 diferente do esperado")
                p = cache / dst.replace("/", "_")
                p.write_bytes(data)
                return p
            except Exception as e:
                erros.append(f"{base.split('/')[2]}: {e}")
                time.sleep(1)
    for pasta in (Path(sys.executable).parent, Path(__file__).parent, Path.cwd()):
        loc = pasta / "arquivos-oficiais" / nome
        if loc.exists() and hashlib.sha256(loc.read_bytes()).hexdigest() == sha:
            log(f"  usando arquivo local: {loc}")
            return loc
    raise RuntimeError(f"Não consegui baixar {rel} (rede/antivírus bloqueando?). Último erro: {erros[-1]}. "
                       f"Alternativa: baixe '{nome}' de {MIRRORS[1]}{rel} e coloque na pasta 'arquivos-oficiais' ao lado do instalador.")


def files_map():
    """origem relativa ao payload -> destino relativo ao jogo (arquivos embutidos)."""
    return {
        "dfhooks.dll": "dfhooks.dll",
        "dfhooks_dfint.dll": "dfhooks_dfint.dll",
        "dfint-data/dictionary.csv": "dfint-data/dictionary.csv",
    }


def install(game, log=print, force=False):
    game = Path(game)
    exe = game / "Dwarf Fortress.exe"
    if not exe.exists():
        raise RuntimeError("Dwarf Fortress.exe não encontrado nessa pasta.")
    ts = pe_timestamp(exe)
    if ts != EXPECTED_TS and not force:
        raise RuntimeError(f"Versão do jogo incompatível (carimbo {ts:#x}, esperado {EXPECTED_TS:#x}). "
                           "Este pacote é para Dwarf Fortress 53.16 Steam. Atualize/regrida o jogo.")
    import tempfile
    cache = Path(tempfile.mkdtemp(prefix="dfptbr_"))
    log("Baixando arquivos oficiais do hook (config, offsets, codificação, fonte)…")
    fontes = {dst: baixar(dst, cache, log) for dst in BAIXAR}
    bk = game / BACKUP
    if (game / LOG).exists():
        log("Instalação anterior detectada; reinstalando por cima (backup original preservado).")
    bk.mkdir(exist_ok=True)
    manifest = {"files": {}, "time": time.strftime("%Y-%m-%d %H:%M:%S")}
    prev = {}
    if (bk / "manifest.json").exists():
        prev = json.loads((bk / "manifest.json").read_text())["files"]
    itens = [(payload_dir() / src, dst) for src, dst in files_map().items()] + [(p, dst) for dst, p in fontes.items()]
    for s, dst in itens:
        d = game / dst
        had = d.exists()
        if dst in prev:                      # backup original ja existe: nao sobrescrever
            manifest["files"][dst] = prev[dst]
        else:
            if had:
                b = bk / dst
                b.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(d, b)
            manifest["files"][dst] = {"had_original": had}
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)
        if hashlib.sha256(s.read_bytes()).digest() != hashlib.sha256(d.read_bytes()).digest():
            raise RuntimeError(f"Falha ao copiar {dst}")
        log(f"  instalado: {dst}")
    (bk / "manifest.json").write_text(json.dumps(manifest, indent=1))
    (game / LOG).write_text(json.dumps({"installed": True, **manifest}, indent=1))
    log("Pronto. Abra o Dwarf Fortress pela Steam normalmente.")


def uninstall(game, log=print):
    game = Path(game)
    bk = game / BACKUP
    mf = bk / "manifest.json"
    if not mf.exists():
        raise RuntimeError("Nada para desinstalar (backup não encontrado).")
    files = json.loads(mf.read_text())["files"]
    for dst, info in files.items():
        d = game / dst
        if info["had_original"]:
            shutil.copy2(bk / dst, d)
            log(f"  restaurado: {dst}")
        elif d.exists():
            d.unlink()
            log(f"  removido: {dst}")
    shutil.rmtree(game / "dfint-data", ignore_errors=True)
    shutil.rmtree(bk, ignore_errors=True)
    (game / LOG).unlink(missing_ok=True)
    log("Tradução removida; jogo restaurado.")


def gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox, scrolledtext
    root = tk.Tk()
    root.title("Dwarf Fortress em Português (PT-BR) — Instalador")
    root.geometry("640x420")
    var = tk.StringVar()
    games = find_game()
    if games:
        var.set(str(games[0]))
    tk.Label(root, text="Pasta do Dwarf Fortress:").pack(anchor="w", padx=10, pady=(10, 0))
    row = tk.Frame(root); row.pack(fill="x", padx=10)
    tk.Entry(row, textvariable=var).pack(side="left", fill="x", expand=True)
    tk.Button(row, text="Procurar…", command=lambda: var.set(filedialog.askdirectory() or var.get())).pack(side="left", padx=4)
    out = scrolledtext.ScrolledText(root, height=15); out.pack(fill="both", expand=True, padx=10, pady=10)

    def log(m):
        out.insert("end", m + "\n"); out.see("end"); root.update()
    if not games:
        log("Jogo não encontrado automaticamente. Escolha a pasta manualmente.")
    else:
        log(f"Jogo encontrado: {games[0]}")

    def run(fn):
        try:
            fn(var.get(), log)
        except Exception as e:
            log(f"ERRO: {e}")
            messagebox.showerror("Erro", str(e))
    b = tk.Frame(root); b.pack(pady=(0, 10))
    tk.Button(b, text="Instalar tradução", width=20, command=lambda: run(install)).pack(side="left", padx=6)
    tk.Button(b, text="Desinstalar", width=16, command=lambda: run(uninstall)).pack(side="left", padx=6)
    root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("install", "uninstall", "find"):
        if sys.argv[1] == "find":
            print("\n".join(map(str, find_game())) or "nenhum")
        else:
            (install if sys.argv[1] == "install" else uninstall)(sys.argv[2])
    else:
        gui()
