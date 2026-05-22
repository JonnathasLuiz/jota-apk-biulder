# Jota APK Builder

Jota APK Builder é um orquestrador de builds na nuvem que permite transformar repositórios Git em arquivos APK prontos para uso. Ele suporta projetos Android nativos (Gradle) e projetos Python/Kivy (Buildozer).

## 🚀 Funcionalidades

- **Automação de Build:** Detecta automaticamente o tipo de projeto e inicia a compilação.
- **Processamento Assíncrono:** Utiliza Celery e Redis para gerenciar builds em segundo plano.
- **API REST:** Interface simples para iniciar builds, consultar status e baixar resultados.
- **Logs em Tempo Real:** Acompanhe o progresso da compilação através dos logs retornados pela API.

## 📚 Documentação

Dividimos nossa documentação para melhor atender às suas necessidades:

- [**Manual do Usuário**](./docs/user/README.md): Como usar a API para compilar seus projetos.
- [**Guia do Desenvolvedor**](./docs/dev/requisitos_e_instalacao.md): Requisitos de sistema, instalação e como contribuir.
- [**Documentação Técnica (AI)**](./docs/ai/README.md): Detalhes de arquitetura e endpoints para agentes de IA.

## 🛠️ Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)
- [Celery](https://docs.celeryq.dev/)
- [Redis](https://redis.io/)
- [Docker](https://www.docker.com/) (Opcional)

## 🤝 Contribuição

Interessado em ajudar? Confira nosso [Guia de Contribuição](./docs/dev/contribuicao.md).
