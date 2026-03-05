import os, glob

src = 'c:/Users/marzabe/GitHub/RiskPredictor-RPA/frontend/src'
files = glob.glob(src + '/**/*.tsx', recursive=True)

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content.replace(
        "'http://127.0.0.1:8000/",
        "`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/"
    ).replace(
        "\"http://127.0.0.1:8000/",
        "`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/"
    ).replace(
        "`http://127.0.0.1:8000/",
        "`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/"
    ).replace(
        "'http://127.0.0.1:8000'",
        "(import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000')"
    ).replace(
        "\"http://127.0.0.1:8000\"",
        "(import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000')"
    ).replace(
        "`http://127.0.0.1:8000`",
        "(import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000')"
    )

    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
