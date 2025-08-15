# 🐳 Docker Setup - Detector de Plágio

## ✅ **Configuração Completa**

A aplicação está agora configurada para rodar no Docker com facilidade!

### **🚀 Início Rápido**

```bash
# 1. Construir e executar (primeira vez)
./docker-manager.sh build
./docker-manager.sh run

# 2. Acessar aplicação
# Abra: http://localhost:8501
```

### **🔧 Script de Gerenciamento**

O `docker-manager.sh` oferece comandos completos:

```bash
# Construir imagem
./docker-manager.sh build

# Iniciar container
./docker-manager.sh run

# Verificar status  
./docker-manager.sh status

# Ver logs em tempo real
./docker-manager.sh logs

# Parar container
./docker-manager.sh stop

# Reconstruir tudo
./docker-manager.sh rebuild
```

### **📊 Status Atual**

```
✅ Container: detector-historia
✅ Imagem: detector-historia-brasil  
✅ Porta: 8501
✅ Status: Rodando
✅ URL: http://localhost:8501
```

### **🌐 Base de Dados**

O container carrega automaticamente:
- **25 artigos** sobre História do Brasil
- **Wikipedia em português**
- **Carregamento inicial**: ~30-60 segundos

### **🔍 Verificações**

```bash
# Ver containers ativos
docker ps

# Ver logs detalhados  
docker logs detector-historia

# Entrar no container (debug)
docker exec -it detector-historia /bin/bash
```

### **🛠️ Troubleshooting**

**Problema**: Porta 8501 ocupada
```bash
./docker-manager.sh stop
./docker-manager.sh run
```

**Problema**: Imagem corrompida
```bash
./docker-manager.sh rebuild
```

**Problema**: Container não responde
```bash
docker logs detector-historia
./docker-manager.sh stop
./docker-manager.sh run
```

---

**🎉 Aplicação rodando no Docker com sucesso!**
