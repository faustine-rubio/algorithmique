# data/vocab_data.py

import csv
import os

# Vocabulaire en mémoire: clé = mot français -> [mot anglais, catégorie, niveau]
vocab = {}


def _data_folder():
	# dossier qui contient ce module (le dossier `data`)
	return os.path.dirname(__file__)


def discover_csv_files():
	folder = _data_folder()
	try:
		return [f for f in os.listdir(folder) if f.lower().endswith('.csv')]
	except Exception:
		return []


def _parse_row(file_name, row):
	# attend au moins french;english ; metadata peut être en colonne 3 ou 4
	french = row[0].strip()
	english = row[1].strip() if len(row) > 1 else ""

	# valeurs par défaut
	category = os.path.splitext(file_name)[0].replace("en-fr_", "")
	level = "basic"

	meta = None
	if len(row) >= 4 and row[3].strip():
		meta = row[3].strip()
	elif len(row) >= 3 and row[2].strip():
		meta = row[2].strip()

	if meta:
		parts = [p.strip() for p in meta.split(',') if p.strip()]
		if len(parts) >= 2:
			level = parts[0]
			category = parts[1]
		elif len(parts) == 1:
			p = parts[0].lower()
			if p in ("basic", "intermediate", "advanced"):
				level = parts[0]
			else:
				category = parts[0]

	return french, english, category, level


def load_all_vocab():
	"""Charge tous les CSV du dossier `data` dans le dictionnaire `vocab`.

	Format attendu des lignes CSV :
	  french;english;;level, category
	Exemple : bon(ne);good;;basic, adjective
	"""
	folder = _data_folder()
	csv_files = discover_csv_files()

	for file in csv_files:
		path = os.path.join(folder, file)
		try:
			with open(path, newline="", encoding="utf-8") as f:
				reader = csv.reader(f, delimiter=';')
				for row in reader:
					if not row:
						continue
					if len(row) >= 2:
						french, english, category, level = _parse_row(file, row)
						vocab[french] = [english, category, level]
		except Exception:
			# ignorer les fichiers non lisibles
			continue


def save_word_to_csv(french, english, category=None, level="basic"):
	"""Enregistre un mot dans le CSV correspondant (crée le fichier s'il n'existe pas).

	Le nom utilisé est `en-fr_<category>.csv` (category normalisée en slug).
	"""
	if not category:
		category = 'custom'
	cat_slug = category.lower().strip().replace(' ', '-')
	if cat_slug in ('unknown', ''):
		cat_slug = 'custom'

	csv_path = os.path.join(_data_folder(), f"en-fr_{cat_slug}.csv")
	meta = f"{level}, {category}"
	with open(csv_path, 'a', newline='', encoding='utf-8') as cf:
		writer = csv.writer(cf, delimiter=';')
		writer.writerow([french, english, '', meta])


def delete_word_from_csv(french, category=None):
	"""Supprime toutes les occurrences du mot français dans les CSV (si category spécifiée, cible d'abord le fichier associé)."""
	folder = _data_folder()
	targets = []
	try:
		files = [f for f in os.listdir(folder) if f.lower().endswith('.csv')]
	except Exception:
		return False

	if category:
		slug = category.lower().strip().replace(' ', '-')
		targets = [os.path.join(folder, f) for f in files if f"en-fr_{slug}" in f.lower()]

	if not targets:
		targets = [os.path.join(folder, f) for f in files]

	removed = False
	for path in targets:
		try:
			rows = []
			changed = False
			with open(path, newline='', encoding='utf-8') as rf:
				reader = csv.reader(rf, delimiter=';')
				for row in reader:
					if not row:
						continue
					first = row[0].strip() if len(row) > 0 else ''
					if first == french:
						changed = True
						removed = True
						continue
					rows.append(row)

			if changed:
				with open(path, 'w', newline='', encoding='utf-8') as wf:
					writer = csv.writer(wf, delimiter=';')
					for r in rows:
						writer.writerow(r)
		except Exception:
			continue

	if removed:
		try:
			del vocab[french]
		except KeyError:
			pass
	return removed


