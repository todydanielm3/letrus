#!/bin/bash
# Script para gerenciar o Detector de Plágio no Docker

set -e

PROJECT_NAME="detector-historia-brasil"
CONTAINER_NAME="detector-historia"
PORT="8501"

case "${1:-help}" in
  "build")
    echo "🔨 Construindo imagem Docker..."
    docker build -f Dockerfile_minimal -t $PROJECT_NAME .
    echo "✅ Imagem construída com sucesso!"
    ;;
    
  "run")
    echo "🚀 Iniciando container..."
    
    # Para container existente se estiver rodando
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
      echo "⏹️  Parando container existente..."
      docker stop $CONTAINER_NAME
      docker rm $CONTAINER_NAME
    fi
    
    # Inicia novo container
    docker run -d -p $PORT:$PORT --name $CONTAINER_NAME $PROJECT_NAME
    echo "✅ Container iniciado!"
    echo "🌐 Acesse: http://localhost:$PORT"
    ;;
    
  "stop")
    echo "⏹️  Parando container..."
    docker stop $CONTAINER_NAME || true
    docker rm $CONTAINER_NAME || true
    echo "✅ Container parado!"
    ;;
    
  "logs")
    echo "📋 Logs do container:"
    docker logs -f $CONTAINER_NAME
    ;;
    
  "status")
    echo "📊 Status do container:"
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
      echo "✅ Container está rodando"
      docker ps -f name=$CONTAINER_NAME
    else
      echo "❌ Container não está rodando"
    fi
    ;;
    
  "rebuild")
    echo "🔄 Reconstruindo e reiniciando..."
    $0 stop
    $0 build
    $0 run
    ;;
    
  "help"|*)
    echo "🇧🇷 Detector de Plágio - História do Brasil"
    echo "=" * 50
    echo "Comandos disponíveis:"
    echo "  build    - Constrói a imagem Docker"
    echo "  run      - Inicia o container"
    echo "  stop     - Para e remove o container"
    echo "  logs     - Mostra logs do container"
    echo "  status   - Verifica status do container"
    echo "  rebuild  - Reconstrói e reinicia tudo"
    echo "  help     - Mostra esta ajuda"
    echo ""
    echo "Exemplo de uso:"
    echo "  ./docker-manager.sh build"
    echo "  ./docker-manager.sh run"
    echo "  ./docker-manager.sh logs"
    ;;
esac
