<#
  StreamView Analytics - Gitflow EA2
  Crea las ramas feature, un commit por rama con sus archivos, y (opcional) las sube a GitHub.

  USO (PowerShell, desde la RAIZ del repositorio clonado, donde esta la carpeta .git):
    1) Copia los archivos nuevos del proyecto sobre tu repositorio (sin commitear).
    2) .\scripts\gitflow_ea2.ps1              # crea develop, las ramas y los commits (todo local)
       .\scripts\gitflow_ea2.ps1 -Subir       # ademas hace push de develop y de cada rama
       .\scripts\gitflow_ea2.ps1 -Subir -CrearPR   # ademas crea los Pull Requests (requiere GitHub CLI: gh)

  Los Pull Requests se fusionan en GitHub (base: develop). Al terminar, vuelve a tu equipo con:
    git checkout develop ; git pull
  Nota: sin -Subir, los archivos de las ramas quedan guardados en las ramas y desaparecen del
  directorio de trabajo hasta que las fusiones en develop (es lo normal en Gitflow).
#>
param([switch]$Subir, [switch]$CrearPR)
$ErrorActionPreference = "Continue"

function Git { & git @args; if ($LASTEXITCODE -ne 0) { throw "git $($args -join ' ') fallo" } }

# --- Comprobaciones previas (con mensajes claros) ---
$dentro = (& git rev-parse --is-inside-work-tree 2>&1)
if ("$dentro" -ne "true") { throw "Esta carpeta no esta dentro de un repositorio Git. Entra a la carpeta del proyecto (la que tiene requirements.txt)." }
if (-not (Test-Path "src/common.py")) { throw "No encuentro src/common.py. Ejecuta el script desde la carpeta streamview-analytics (la que tiene requirements.txt)." }
$correo = (& git config user.email)
if (-not $correo) { throw 'Falta tu identidad de Git. Ejecuta: git config --global user.name "Tu Nombre"  y  git config --global user.email "tu-correo-de-github"' }
& git rev-parse --verify HEAD *> $null
if ($LASTEXITCODE -ne 0) { throw "El repositorio no tiene ningun commit base. Haz primero el commit base con el proyecto EA1 (ver docs/gitflow.md)." }
$base = if (& git branch --list main) { "main" } else { "master" }

$ramas = @(
  @{ n = "feature/data-uid-calificacion"; m = "feat(datos): agrega uid, calificacion valida y percentil de popularidad";
     a = @("src/common.py", "src/data/clean_data.py", "reports/data_quality/cleaning_summary.csv", "requirements.txt") },
  @{ n = "feature/dashboard-base"; m = "feat(dashboard): portada y utilidades compartidas (filtros, formato, agregaciones)";
     a = @("dashboard/__init__.py", "dashboard/utils.py", "dashboard/app.py") },
  @{ n = "feature/dashboard-ejecutivo"; m = "feat(ejecutivo): dashboard ejecutivo con KPIs, filtros, mapa y evolucion";
     a = @("dashboard/pages/1_Ejecutivo.py") },
  @{ n = "feature/dashboard-analitico"; m = "feat(analitico): dashboard analitico con bloque financiero y conclusiones";
     a = @("dashboard/pages/2_Analitico.py") },
  @{ n = "feature/d3-treemap"; m = "feat(d3): treemap de generos en D3 incrustado en Streamlit";
     a = @("src/d3_treemap.py", "src/export/__init__.py", "src/export/build_d3.py", "d3") },
  @{ n = "feature/dash-financiero"; m = "feat(dash): dashboard financiero de peliculas en Dash";
     a = @("dash_app") },
  @{ n = "feature/seaborn-eda"; m = "feat(seaborn): mapa de correlaciones y distribucion de calificacion";
     a = @("src/analysis/eda_seaborn.py", "images/eda/10_correlaciones.png", "images/eda/11_distribucion_calificacion.png") },
  @{ n = "feature/powerbi"; m = "feat(powerbi): modelo en estrella, consultas M, medidas DAX y guia";
     a = @("src/export/export_powerbi.py", "powerbi") },
  @{ n = "feature/docs-ea2"; m = "docs(ea2): README, arquitectura, justificacion, gitflow, guion y plantilla de PR";
     a = @("README.md", "docs", ".github", "notebooks/01_analisis_completo.py", "scripts") }
)

# develop nace de main
Git checkout $base
if ($Subir -and (& git remote)) { Git pull }
$existe = (& git branch --list develop)
if ($existe) { Git checkout develop } else { Git checkout -b develop }
if ($Subir) { Git push -u origin develop }

foreach ($r in $ramas) {
  Write-Host "`n=== $($r.n) ===" -ForegroundColor Cyan
  Git checkout develop
  Git checkout -b $r.n
  $presentes = @($r.a | Where-Object { Test-Path $_ })
  if ($presentes.Count -eq 0) { Write-Host "Sin archivos para esta rama; se omite." -ForegroundColor Yellow; Git checkout develop; Git branch -D $r.n; continue }
  Git add -- $presentes
  Git commit -m $r.m
  if ($Subir) { Git push -u origin $r.n }
  if ($Subir -and $CrearPR) {
    if (Get-Command gh -ErrorAction SilentlyContinue) {
      & gh pr create --base develop --head $r.n --title $r.m --body-file ".github/pull_request_template.md"
    } else { Write-Host "GitHub CLI (gh) no esta instalado: crea el PR a mano en GitHub." -ForegroundColor Yellow }
  }
}
Git checkout develop
Write-Host "`nListo. Ramas creadas:" -ForegroundColor Green
Git branch
Write-Host "Siguiente paso: abrir/fusionar los Pull Requests hacia develop en GitHub; luego PR develop -> main y tag v2.0-ea2 (ver docs/gitflow.md)."
