# 🎵 MP3-Tagger

A Python script that automatically finds and applies metadata tags to your MP3 files — including album cover art, title, artist, and more — using the Last.fm API.

> 🌐 **Available in:** [English](#-mp3-tagger) | [Italiano](#-mp3-tagger-1)

---

## ✨ Features

- Automatically fetches metadata (title, artist, album, cover art, etc.) for MP3 files
- Simple and intuitive GUI — no command line needed
- Batch process an entire folder of MP3 files at once
- Outputs tagged files to a dedicated folder on your Desktop
- 🌐 GUI available in **English** and **Italian**

---

## 📋 Requirements

- Python 3.x
- A free Last.fm API key
- The following Python libraries:
  ```
  mutagen
  requests
  ```

---

## 🚀 Setup

### 1. Get a Last.fm API Key

Create a free API account at:
👉 [https://www.last.fm/api/account/create](https://www.last.fm/api/account/create)

### 2. Add your API Key to the script

Open the script and paste your API key at **line 18**:

```python
LASTFM_API_KEY = "your_api_key_here"
```

### 3. Install dependencies

Run the following command in your terminal:

```bash
pip install mutagen requests
```

---

## 🖥️ Usage

1. Run the script:
   ```bash
   python mp3_tagger.py
   ```
2. A GUI window will open.
3. Use the interface to **select the folder** containing your MP3 files.
4. Click **"Avvia Tagging"** to start the process.
5. Once complete, find your tagged MP3 files in a new folder on your Desktop:
   ```
   ~/Desktop/MP3-Tagger-Output/
   ```

---

## 📁 Output

Tagged files are saved to a new folder called **`MP3-Tagger-Output`** on your Desktop. Your original files are left untouched.

---

## 🛠️ Dependencies

| Library | Purpose |
|--------|---------|
| `mutagen` | Reading and writing MP3 metadata tags |
| `requests` | Making API calls to Last.fm |

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute it.

---
---

# 🎵 MP3-Tagger

Uno script Python che trova e applica automaticamente i tag ai tuoi file MP3 — copertina dell'album, titolo, artista e altro — tramite l'API di Last.fm.

> 🌐 **Disponibile in:** [English](#-mp3-tagger) | [Italiano](#-mp3-tagger-1)

---

## ✨ Funzionalità

- Recupera automaticamente i metadati (titolo, artista, album, copertina, ecc.) per i file MP3
- Interfaccia grafica semplice e intuitiva — nessuna riga di comando necessaria
- Elaborazione in batch di un'intera cartella di file MP3
- Salva i file taggati in una cartella dedicata sul Desktop
- 🌐 Interfaccia disponibile in **italiano** e **inglese**

---

## 📋 Requisiti

- Python 3.x
- Una API key gratuita di Last.fm
- Le seguenti librerie Python:
  ```
  mutagen
  requests
  ```

---

## 🚀 Configurazione

### 1. Ottieni una API Key di Last.fm

Crea un account API gratuito su:
👉 [https://www.last.fm/api/account/create](https://www.last.fm/api/account/create)

### 2. Aggiungi la tua API Key allo script

Apri lo script e incolla la tua chiave alla **riga 18**:

```python
LASTFM_API_KEY = "la_tua_api_key_qui"
```

### 3. Installa le dipendenze

Esegui il seguente comando nel terminale:

```bash
pip install mutagen requests
```

---

## 🖥️ Utilizzo

1. Avvia lo script:
   ```bash
   python mp3_tagger.py
   ```
2. Si aprirà una finestra con l'interfaccia grafica.
3. Usa l'interfaccia per **selezionare la cartella** contenente i tuoi file MP3.
4. Clicca su **"Avvia Tagging"** per iniziare il processo.
5. Al termine, troverai i tuoi MP3 taggati in una nuova cartella sul Desktop:
   ```
   ~/Desktop/MP3-Tagger-Output/
   ```

---

## 📁 Output

I file taggati vengono salvati in una nuova cartella chiamata **`MP3-Tagger-Output`** sul Desktop. I file originali non vengono modificati.

---

## 🛠️ Dipendenze

| Libreria | Scopo |
|----------|-------|
| `mutagen` | Lettura e scrittura dei tag MP3 |
| `requests` | Chiamate API a Last.fm |

---

## 📄 Licenza

Questo progetto è open source. Sentiti libero di usarlo, modificarlo e distribuirlo.
