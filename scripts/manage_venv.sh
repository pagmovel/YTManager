#!/bin/bash
# scripts/manage_venv.sh
# Script para verificar se o ambiente virtual existe e está ativado

check_venv() {
    # Verifica se o diretório .venv existe
    if [ ! -d ".venv" ]; then
        echo "Ambiente virtual não encontrado. Criando..."
        python -m venv .venv
        echo "Ambiente virtual criado em .venv"
    fi

    # Ativa o ambiente virtual se não estiver ativado
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "Ativando ambiente virtual..."
        source .venv/bin/activate
        echo "Ambiente virtual ativado"
    else
        if [[ "$VIRTUAL_ENV" == *"$(pwd)/.venv"* ]]; then
            echo "Ambiente virtual já está ativado"
        else
            echo "Desativando ambiente virtual atual..."
            deactivate 2>/dev/null || true
            echo "Ativando ambiente virtual do projeto..."
            source .venv/bin/activate
            echo "Ambiente virtual ativado"
        fi
    fi
}

check_venv