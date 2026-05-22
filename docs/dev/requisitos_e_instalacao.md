# Requisitos e Instalação - Jota APK Builder

Este documento descreve os pré-requisitos e o processo de instalação para colaboradores e usuários que desejam hospedar sua própria instância do Jota APK Builder.

## 1. Requisitos de Hardware

O processo de compilação de APKs (Android) é exigente em termos de recursos.
- **Processador:** Mínimo de 2 núcleos (4+ recomendados).
- **Memória RAM:** Mínimo de 8GB (Compilações Gradle e Buildozer podem falhar com menos devido ao consumo da JVM).
- **Espaço em Disco:** Pelo menos 20GB livres (para Android SDK, NDK, caches do Gradle e imagens de build).

## 2. Requisitos de Software

### Essenciais
- **Sistema Operacional:** Linux (Ubuntu 20.04+ recomendado) ou macOS. (Windows requer WSL2).
- **Python:** 3.9 ou superior.
- **Redis:** Para gerenciamento da fila de tarefas do Celery.
- **Git:** Para clonar os repositórios que serão compilados.

### Para Compilação Android
- **Java Development Kit (JDK):** JDK 11 ou 17.
- **Android SDK:** Command line tools instalados.
- **Android NDK:** Necessário especialmente para projetos Kivy/Python.

## 3. Instalação Passo a Passo

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/jota-apk-builder.git
cd jota-apk-builder
```

### Passo 2: Configurar Ambiente Python
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Passo 3: Configurar o Redis
Certifique-se de que o Redis está rodando. Por padrão, o sistema procura por `redis://localhost:6379/0`.
Você pode alterar isso definindo a variável de ambiente `REDIS_URL`.

### Passo 4: Preparar Diretórios de Armazenamento
O sistema armazena os APKs gerados em `./storage/apks/`.
```bash
mkdir -p storage/apks
```

### Passo 5: Iniciar os Serviços

Você precisará de dois terminais (ou rodar em background):

**Terminal 1: Celery Worker (Processador de Builds)**
```bash
celery -A app.worker.celery_app worker --loglevel=info
```

**Terminal 2: FastAPI (API do Servidor)**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 4. Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `REDIS_URL` | URL de conexão com o Redis | `redis://localhost:6379/0` |
| `STORAGE_PATH` | Caminho para salvar APKs | `./storage/apks/` |

## 5. Solução de Problemas Comuns

- **Erro de Memória (Out of Memory):** Aumente o SWAP ou a RAM disponível. Compilações Android são pesadas.
- **Gradle não encontrado:** O sistema tenta usar o `gradlew` do repositório. Certifique-se de que o repositório clonado tenha permissões de execução.
- **Buildozer falhando:** Verifique se todas as dependências do sistema para Kivy (zlib, libffi, etc.) estão instaladas.
