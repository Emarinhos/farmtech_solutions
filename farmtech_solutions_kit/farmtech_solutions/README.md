# FarmTech Solutions Project
## Como rodar (Windows + VS Code)

### Python
```powershell
.\venv\Scripts\activate.bat
python python\app.py

# menu: inserir 2 registros (soja/milho) e opção 5 para exportar CSV

#Após inserir os registros
$RS = "C:\Program Files\R\R-4.5.1\bin\Rscript.exe"
& $RS .\r\setup_pkgs.R     # (uma vez)
& $RS .\r\analysis.R
& $RS .\r\weather.R -23.42 -51.94 7

## 3) (Opcional) Task no VS Code para rodar R com 1 clique
Crie `.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "R - analysis",
      "type": "shell",
      "command": "C:\\Program Files\\R\\R-4.5.1\\bin\\Rscript.exe",
      "args": ["r/analysis.R"]
    },
    {
      "label": "R - weather (Maringá 7d)",
      "type": "shell",
      "command": "C:\\Program Files\\R\\R-4.5.1\\bin\\Rscript.exe",
      "args": ["r/weather.R", "-23.42", "-51.94", "7"]
    }
  ]
}