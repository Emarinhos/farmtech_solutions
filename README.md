

# Farmtech projeto.
## FarmTech Solutions Project
### Como rodar 

#### Python
```powershell
.\venv\Scripts\activate.bat
python python\app.py

# menu: inserir 2 registros (soja/milho) e opção 5 para exportar CSV
##### R
#Após inserir os registros
$RS = "C:\Program Files\R\R-4.5.1\bin\Rscript.exe"
& $RS .\r\setup_pkgs.R     # (uma vez)
& $RS .\r\analysis.R
& $RS .\r\weather.R -23.42 -51.94 7

d050722 (chore(repo): migrar raiz do repositório para farmtech_solutions/)
