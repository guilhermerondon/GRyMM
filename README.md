# GRyMM


# 🏋️ Gerenciador de Academias & Alunos (Fitness API)

API REST para gerenciamento de **alunos, treinos e exercícios**, com integração a uma **API externa de exercícios**, regras de negócio bem definidas e foco em arquitetura limpa.

Projeto desenvolvido em **Python**, totalmente backend, com pipeline de qualidade já configurada.

---

## 📌 Funcionalidades

### 👤 Alunos
- Cadastro de alunos
- Atualização e remoção
- Listagem e consulta individual

### 🏋️ Treinos
- Criação de treinos para alunos
- Um aluno **não pode ter mais de um treino ativo**
- Associação de exercícios ao treino
- Comparação de treinos (mais pesado, mais intenso, etc.)
- Endpoint de **desafio entre treinos**

### 🧠 Exercícios
- Integração com API pública de exercícios
- Envio apenas do **nome do exercício**
- Demais dados vêm automaticamente da API externa:
  - Grupo muscular
  - Dificuldade
  - GIF / imagem
- Cache das chamadas externas para melhor performance

### 📊 Relatórios (bônus)
- Quantidade de alunos
- Treinos ativos
- Volume total de carga por aluno

---
