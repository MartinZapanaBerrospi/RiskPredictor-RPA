import os, glob

src = 'c:/Users/marzabe/GitHub/RiskPredictor-RPA/frontend/src'
files = glob.glob(src + '/**/*.tsx', recursive=True)

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The previous script did this:
    # "`${import.meta.env.VITE_API_URL || (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000')}/predict', {"
    # We want: 
    # "`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/predict`"
    
    # First, let's fix the double-injection messes
    content = content.replace(
        "`${import.meta.env.VITE_API_URL || (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000')}/",
        "`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/"
    )
    
    # Now, the issue is that the replacement ended with /predict', which leaves it as:
    # `${...}/predict',
    # Which is a template string opened but closed with single quote.
    
    # Let's fix the specific fetch calls manually to ensure they are correct:
    # 1. App.tsx
    # fetch(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/predict',
    # -> fetch(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/predict`,
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if "`$" in line and "', {" in line:
             line = line.replace("', {", "`, {")
        elif "`$" in line and "'," in line:
             line = line.replace("',", "`,")
        elif "`$" in line and "';" in line:
             line = line.replace("';", "`;")
        elif "`$" in line and "')" in line:
             line = line.replace("')", "`)")
             
        # Fix specific cases with double quotes at the end of string
        if "`$" in line and "\", {" in line:
             line = line.replace("\", {", "`, {")
        elif "`$" in line and "\");" in line:
             line = line.replace("\");", "`);")
        elif "`$" in line and "\")" in line:
             line = line.replace("\")", "`)")
             
        new_lines.append(line)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
        
    print(f"Fixed {filepath}")
