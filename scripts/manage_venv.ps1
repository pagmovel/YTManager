# scripts/manage_venv.ps1
# Script para verificar se o ambiente virtual existe e está ativado

function Check-Venv {
    # Verifica se o diretório .venv existe
    if (-not (Test-Path -Path ".venv")) {
        Write-Host "Ambiente virtual não encontrado. Criando..."
        python -m venv .venv
        Write-Host "Ambiente virtual criado em .venv"
    }

    # Verifica se o ambiente virtual está ativado
    $venvActive = $env:VIRTUAL_ENV
    if (-not $venvActive) {
        Write-Host "Ativando ambiente virtual..."
        & .\.venv\Scripts\Activate.ps1
        Write-Host "Ambiente virtual ativado"
    }
    else {
        $projectPath = (Get-Location).Path + "\.venv"
        if ($venvActive -like "*$projectPath*") {
            Write-Host "Ambiente virtual já está ativado"
        }
        else {
            Write-Host "Desativando ambiente virtual atual..."
            deactivate
            Write-Host "Ativando ambiente virtual do projeto..."
            & .\.venv\Scripts\Activate.ps1
            Write-Host "Ambiente virtual ativado"
        }
    }
}

Check-Venv