# Guia de Contribuição - Jota APK Builder

Obrigado por seu interesse em contribuir para o Jota APK Builder! Este guia ajudará você a configurar seu ambiente de desenvolvimento e entender o processo de contribuição.

## 1. Configurando o Ambiente de Desenvolvimento

Siga os passos de instalação descritos em [Requisitos e Instalação](./requisitos_e_instalacao.md), mas certifique-se de instalar as dependências de desenvolvimento (se houver).

## 2. Estrutura do Projeto

- `app/main.py`: Pontos de entrada da API FastAPI.
- `app/tasks.py`: Lógica de compilação dos APKs (Android/Kivy).
- `app/worker.py`: Configuração do Celery.
- `docs/`: Documentação do projeto (Usuário, Desenvolvedor, AI).
- `tests/`: Testes automatizados.

## 3. Rodando Testes

Usamos o `pytest` para testes unitários e de integração.
Para rodar todos os testes:

```bash
python3 -m pytest tests/
```

Antes de enviar um Pull Request, certifique-se de que todos os testes estão passando.

## 4. Padronização de Código

- Siga o **PEP 8** para código Python.
- Documente novas funções e classes.
- Mantenha a documentação atualizada ao adicionar novas funcionalidades.

## 5. Processo de Pull Request

1. Faça um Fork do repositório.
2. Crie uma branch para sua funcionalidade (`git checkout -b feature/nova-funcionalidade`).
3. Faça commit das suas alterações com mensagens claras.
4. Faça push para a sua branch (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request detalhando suas mudanças.

## 6. Reportando Bugs

Ao reportar um bug, inclua:
- Passos para reproduzir o erro.
- Logs do sistema (especialmente os logs do Celery worker).
- Informações sobre o ambiente (SO, versão do Python).
