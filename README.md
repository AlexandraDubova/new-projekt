# Flappy Bird – Python (Pygame)

Tento projekt je vlastní implementace jednoduché 2D hry inspirované hrou **Flappy Bird**, vytvořená v jazyce **Python** s využitím knihovny **Pygame**.  
Projekt slouží především jako studijní práce zaměřená na herní logiku, práci s událostmi, sprite objekty a stavový systém hry.

---

## 🎮 Popis hry
Hráč ovládá ptáka, který musí prolétat mezi překážkami (rourami) bez kolize.  
Cílem hry je dosáhnout co nejvyššího skóre.

Hra obsahuje:
- hlavní menu
- nastavení obtížnosti
- přepínání dark/light módu
- zapínání a vypínání zvuků
- herní obrazovku a obrazovku „Game Over“

---

## ⚙️ Ovládání
- **Kliknutí myší** – pohyb ptáka nahoru
- Ovládání menu a nastavení probíhá kliknutím myší

---

## 🛠 Použité technologie
- **Python 3**
- **Pygame**

---

## 📂 Struktura projektu
projekt/
│── main.py # spuštění hry
│── game.py # hlavní herní logika a stavový systém
│── player.py # třída ptáka
│── pipe.py # třída rour
│── button.py # tlačítka v menu
│── settings.py # globální nastavení
│
├── img/ # grafické assety
├── audio/ # zvukové efekty


---

## 🔊 Funkce navíc
- **Nastavení obtížnosti** (Easy / Medium / Hard)
- **Dark mode**
- **Zvuky (ON / OFF)**

---

## ℹ️ Poznámka
Projekt je inspirován existující hrou *Flappy Bird*, avšak veškerý kód byl vytvořen samostatně jako studijní práce.  
Cílem projektu nebylo vytvořit originální herní koncept, ale naučit se principy vývoje her v knihovně Pygame.

---

## ▶️ Spuštění projektu
1. Nainstaluj Python 3
2. Nainstaluj Pygame: pip install pygame
