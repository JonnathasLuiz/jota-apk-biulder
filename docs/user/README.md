# Manual do Usuário - Jota APK Builder

Bem-vindo ao Jota APK Builder! Esta ferramenta permite que você transforme seu repositório Git em um arquivo APK pronto para instalação de forma automatizada.

## Como Usar

### 1. Iniciar um Build
Envie uma requisição POST para o endpoint de build com a URL do seu repositório.

**Endpoint:** `POST /api/v1/build`
**Corpo (JSON):**
```json
{
  "repo_url": "https://github.com/seu-usuario/seu-projeto.git"
}
```
**Resposta:** Você receberá um `task_id`. Guarde-o para consultar o status.

### 2. Verificar o Status
Como builds de APK podem demorar entre 2 a 15 minutos, você deve consultar o status periodicamente.

**Endpoint:** `GET /api/v1/status/{task_id}`
**Resposta:**
- `PENDING`: Aguardando na fila.
- `PROCESSING`: O build está em andamento.
- `SUCCESS`: O build terminou com sucesso! Um `download_url` será fornecido.
- `FAILED`: O build falhou. Verifique o campo `logs` para entender o motivo.

### 3. Baixar o APK
Assim que o status for `SUCCESS`, você pode baixar o arquivo.

**Endpoint:** `GET /api/v1/download/{task_id}`

## Requisitos do Repositório
Para que o sistema identifique seu projeto, ele deve seguir uma destas estruturas:

- **Android Nativo:** Deve conter um arquivo `build.gradle` ou `build.gradle.kts`.
- **Kivy/Python:** Deve conter um arquivo `buildozer.spec`.

## Notas Importantes
- Certifique-se de que o repositório seja público ou acessível sem autenticação SSH/HTTPS personalizada no momento.
- Os arquivos APK são identificados pelo ID da tarefa.
