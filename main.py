#!/usr/bin/env python3

import sys
import shutil
import re
import requests
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path
import threading
import urllib.request

try:
    from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC, ID3NoHeaderError
except ImportError:
    sys.exit("Install mutagen:  pip install mutagen")

LASTFM_API_KEY = "a75ba6bd2a4e81482c2db22e8cc0e4b0"
LASTFM_BASE    = "https://ws.audioscrobbler.com/2.0/"
OUTPUT_BASE    = Path.home() / "Desktop" / "MP3-Tagger-Output"

STRINGS = {
    "it": {
        "title":         "MP3 Tagger",
        "subtitle":      "Cerca & applica tag via Last.fm",
        "api_label":     "API Key Last.fm:",
        "src_label":     "Cartella sorgente:",
        "browse":        "Sfoglia...",
        "output_label":  "Output:",
        "start_btn":     "▶  Avvia tagging",
        "err_api":       "Inserisci la tua API key di Last.fm.",
        "err_src":       "Seleziona una cartella sorgente valida.",
        "err_title":     "Errore",
        "no_mp3":        "❌  Nessun file MP3 trovato nella cartella selezionata.",
        "found":         "🔍  Trovati {n} file MP3 – inizio tagging...",
        "searching":     "  🔎  Cerco: '{q}'",
        "not_found":     "  ⚠️  Non trovato su Last.fm – copio senza tag.",
        "cover_ok":      "scaricata",
        "cover_ko":      "non disponibile",
        "cover_line":    "  🖼️  Copertina: {s}",
        "no_cover":      "  🖼️  Nessuna copertina trovata.",
        "album_line":    "  💿  Album: {a}",
        "tag_err":       "  ❌  Errore tag: {e}",
        "done_sep":      "=" * 50,
        "done_log":      "✅  Completato!  OK: {ok}  |  Saltati: {skip}  |  Errori: {err}",
        "done_path":     "📁  Output salvato in: {p}",
        "done_title":    "Fatto!",
        "done_msg":      "Tagging completato!\n\nOK: {ok}  |  Saltati: {skip}  |  Errori: {err}\n\nOutput: {p}",
        "folder_dialog": "Seleziona la cartella con le canzoni",
    },
    "en": {
        "title":         "MP3 Tagger",
        "subtitle":      "Search & apply tags via Last.fm",
        "api_label":     "Last.fm API Key:",
        "src_label":     "Source folder:",
        "browse":        "Browse...",
        "output_label":  "Output:",
        "start_btn":     "▶  Start tagging",
        "err_api":       "Please enter your Last.fm API key.",
        "err_src":       "Please select a valid source folder.",
        "err_title":     "Error",
        "no_mp3":        "❌  No MP3 files found in the selected folder.",
        "found":         "🔍  Found {n} MP3 files – starting tagging...",
        "searching":     "  🔎  Searching: '{q}'",
        "not_found":     "  ⚠️  Not found on Last.fm – copying without tags.",
        "cover_ok":      "downloaded",
        "cover_ko":      "unavailable",
        "cover_line":    "  🖼️  Cover: {s}",
        "no_cover":      "  🖼️  No cover art found.",
        "album_line":    "  💿  Album: {a}",
        "tag_err":       "  ❌  Tag error: {e}",
        "done_sep":      "=" * 50,
        "done_log":      "✅  Done!  OK: {ok}  |  Skipped: {skip}  |  Errors: {err}",
        "done_path":     "📁  Output saved to: {p}",
        "done_title":    "Done!",
        "done_msg":      "Tagging complete!\n\nOK: {ok}  |  Skipped: {skip}  |  Errors: {err}\n\nOutput: {p}",
        "folder_dialog": "Select the folder containing the songs",
    },
}


def clean_filename(name: str) -> str:
    name = Path(name).stem
    name = re.sub(r"[\._\-]+", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def search_track(query: str) -> dict | None:
    params = {
        "method":  "track.search",
        "track":   query,
        "api_key": LASTFM_API_KEY,
        "format":  "json",
        "limit":   1,
    }
    try:
        r = requests.get(LASTFM_BASE, params=params, timeout=10)
        r.raise_for_status()
        tracks = r.json().get("results", {}).get("trackmatches", {}).get("track", [])
        if tracks:
            return tracks[0]
    except Exception:
        pass
    return None


def get_track_info(artist: str, title: str) -> dict:
    params = {
        "method":      "track.getInfo",
        "artist":      artist,
        "track":       title,
        "api_key":     LASTFM_API_KEY,
        "format":      "json",
        "autocorrect": 1,
    }
    try:
        r = requests.get(LASTFM_BASE, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("track", {})
    except Exception:
        pass
    return {}


def best_image_url(images: list) -> str | None:
    size_order = ["extralarge", "large", "medium", "small"]
    by_size = {img.get("size"): img.get("#text") for img in images}
    for s in size_order:
        url = by_size.get(s, "")
        if url and not url.endswith("2a96cbd8b46e442fc41c2b86b821562f.png"):
            return url
    return None


def download_image(url: str) -> bytes | None:
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return resp.read()
    except Exception:
        pass
    return None


def tag_mp3(src: Path, dst: Path, info: dict, cover_data: bytes | None):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    try:
        tags = ID3(str(dst))
    except ID3NoHeaderError:
        tags = ID3()
    title  = info.get("title", "")
    artist = info.get("artist", "")
    album  = info.get("album", {}).get("title", "") if isinstance(info.get("album"), dict) else ""
    if title:
        tags["TIT2"] = TIT2(encoding=3, text=title)
    if artist:
        tags["TPE1"] = TPE1(encoding=3, text=artist)
    if album:
        tags["TALB"] = TALB(encoding=3, text=album)
    if cover_data:
        tags["APIC:"] = APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=cover_data)
    tags.save(str(dst), v2_version=3)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.configure(bg="#1a1a2e")
        self._lang = "it"
        self._widgets = {}
        self._build_ui()
        self._apply_lang()

    def _t(self, key, **kw):
        s = STRINGS[self._lang][key]
        return s.format(**kw) if kw else s

    def _build_ui(self):
        BG  = "#1a1a2e"
        FG  = "#e0e0e0"
        ACC = "#e94560"
        BTN = dict(bg=ACC, fg="white", relief="flat",
                   font=("Helvetica", 11, "bold"), cursor="hand2",
                   activebackground="#c73652", activeforeground="white",
                   padx=14, pady=6)
        PAD = dict(padx=18, pady=8)

        top_bar = tk.Frame(self, bg=BG)
        top_bar.pack(fill="x", padx=18, pady=(14, 0))
        tk.Label(top_bar, text="Lingua / Language:", bg=BG, fg="#888",
                 font=("Helvetica", 9)).pack(side="right", padx=(6, 0))
        self._lang_var = tk.StringVar(value="it")
        lang_cb = ttk.Combobox(top_bar, textvariable=self._lang_var,
                               values=["it", "en"], width=4, state="readonly")
        lang_cb.pack(side="right")
        lang_cb.bind("<<ComboboxSelected>>", self._on_lang_change)

        self._widgets["title_lbl"] = tk.Label(self, bg=BG, fg=ACC, font=("Helvetica", 22, "bold"))
        self._widgets["title_lbl"].pack(pady=(8, 2))

        self._widgets["subtitle_lbl"] = tk.Label(self, bg=BG, fg="#888", font=("Helvetica", 10))
        self._widgets["subtitle_lbl"].pack(pady=(0, 16))

        frm_key = tk.Frame(self, bg=BG)
        frm_key.pack(fill="x", **PAD)
        self._widgets["api_lbl"] = tk.Label(frm_key, bg=BG, fg=FG, font=("Helvetica", 10))
        self._widgets["api_lbl"].pack(anchor="w")
        self.api_var = tk.StringVar()
        tk.Entry(frm_key, textvariable=self.api_var, width=52,
                 bg="#16213e", fg=FG, insertbackground=FG,
                 relief="flat", font=("Courier", 10)).pack(fill="x", pady=4)

        frm_src = tk.Frame(self, bg=BG)
        frm_src.pack(fill="x", **PAD)
        self._widgets["src_lbl"] = tk.Label(frm_src, bg=BG, fg=FG, font=("Helvetica", 10))
        self._widgets["src_lbl"].pack(anchor="w")
        row = tk.Frame(frm_src, bg=BG)
        row.pack(fill="x")
        self.src_var = tk.StringVar()
        tk.Entry(row, textvariable=self.src_var, width=40,
                 bg="#16213e", fg=FG, insertbackground=FG,
                 relief="flat", font=("Helvetica", 10)).pack(side="left", fill="x", expand=True)
        self._widgets["browse_btn"] = tk.Button(row, command=self._pick_folder, **BTN)
        self._widgets["browse_btn"].pack(side="left", padx=(8, 0))

        self._widgets["out_lbl"] = tk.Label(self, bg=BG, fg="#666", font=("Helvetica", 9))
        self._widgets["out_lbl"].pack(pady=(2, 12))

        self._widgets["start_btn"] = tk.Button(self, command=self._start, **BTN)
        self._widgets["start_btn"].pack(pady=(0, 14))

        frm_log = tk.Frame(self, bg=BG)
        frm_log.pack(fill="both", expand=True, padx=18, pady=(0, 6))
        self.log = tk.Text(frm_log, height=16, bg="#0f3460", fg="#a8d8ea",
                           font=("Courier", 9), relief="flat", state="disabled", wrap="word")
        sb = tk.Scrollbar(frm_log, command=self.log.yview)
        self.log.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.log.pack(fill="both", expand=True)

        self.progress = ttk.Progressbar(self, mode="determinate",
                                        style="red.Horizontal.TProgressbar")
        self.progress.pack(fill="x", padx=18, pady=(4, 18))
        sty = ttk.Style()
        sty.theme_use("default")
        sty.configure("red.Horizontal.TProgressbar",
                      troughcolor="#16213e", background=ACC, thickness=8)

    def _apply_lang(self):
        self.title(self._t("title"))
        self._widgets["title_lbl"].config(text=self._t("title"))
        self._widgets["subtitle_lbl"].config(text=self._t("subtitle"))
        self._widgets["api_lbl"].config(text=self._t("api_label"))
        self._widgets["src_lbl"].config(text=self._t("src_label"))
        self._widgets["browse_btn"].config(text=self._t("browse"))
        self._widgets["out_lbl"].config(text=f"{self._t('output_label')} {OUTPUT_BASE}")
        self._widgets["start_btn"].config(text=self._t("start_btn"))

    def _on_lang_change(self, _=None):
        self._lang = self._lang_var.get()
        self._apply_lang()

    def _pick_folder(self):
        d = filedialog.askdirectory(title=self._t("folder_dialog"))
        if d:
            self.src_var.set(d)

    def _log(self, msg: str):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")
        self.update_idletasks()

    def _start(self):
        api_key = self.api_var.get().strip()
        src     = self.src_var.get().strip()
        if not api_key:
            messagebox.showerror(self._t("err_title"), self._t("err_api"))
            return
        if not src or not Path(src).is_dir():
            messagebox.showerror(self._t("err_title"), self._t("err_src"))
            return
        global LASTFM_API_KEY
        LASTFM_API_KEY = api_key
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")
        threading.Thread(target=self._run, args=(Path(src),), daemon=True).start()

    def _run(self, src_root: Path):
        mp3_files = list(src_root.rglob("*.mp3"))
        if not mp3_files:
            self._log(self._t("no_mp3"))
            return

        total = len(mp3_files)
        self.progress["maximum"] = total
        self.progress["value"]   = 0
        self._log(self._t("found", n=total))
        self._log("")

        ok = err = skip = 0

        for i, mp3 in enumerate(mp3_files, 1):
            rel   = mp3.relative_to(src_root)
            dst   = OUTPUT_BASE / rel
            query = clean_filename(mp3.name)

            self._log(f"[{i}/{total}] {rel}")
            self._log(self._t("searching", q=query))

            result = search_track(query)
            if not result:
                self._log(self._t("not_found"))
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(mp3, dst)
                skip += 1
            else:
                title  = result.get("name", query)
                artist = result.get("artist", "")
                self._log(f"  ✅  {artist} - {title}")

                info      = get_track_info(artist, title)
                album     = info.get("album", {}).get("title", "") if isinstance(info.get("album"), dict) else ""
                images    = info.get("album", {}).get("image", []) if isinstance(info.get("album"), dict) else []
                cover_url = best_image_url(images)

                cover_data = None
                if cover_url:
                    cover_data = download_image(cover_url)
                    status = self._t("cover_ok") if cover_data else self._t("cover_ko")
                    self._log(self._t("cover_line", s=status))
                else:
                    self._log(self._t("no_cover"))

                if album:
                    self._log(self._t("album_line", a=album))

                try:
                    tag_mp3(mp3, dst, {"title": title, "artist": artist, "album": {"title": album}}, cover_data)
                    ok += 1
                except Exception as e:
                    self._log(self._t("tag_err", e=e))
                    err += 1

            self.progress["value"] = i
            self._log("")

        self._log(self._t("done_sep"))
        self._log(self._t("done_log", ok=ok, skip=skip, err=err))
        self._log(self._t("done_path", p=OUTPUT_BASE))
        messagebox.showinfo(
            self._t("done_title"),
            self._t("done_msg", ok=ok, skip=skip, err=err, p=OUTPUT_BASE)
        )


if __name__ == "__main__":
    App().mainloop()
