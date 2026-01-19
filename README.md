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
# 📚 API – CRUD de Alunos

Este módulo é responsável pelo **gerenciamento de alunos** dentro da aplicação, disponibilizando operações completas de **CRUD (Create, Read, Update e Delete)** através de uma API REST.

No momento, **não há restrições de autenticação ou permissão**, ou seja, todas as rotas estão públicas para facilitar o desenvolvimento inicial.

---

## 🧩 Recurso: Aluno

### 🔹 Campos do Aluno
| Campo | Tipo | Descrição |
|------|------|-----------|
| `id` | Integer | Identificador único do aluno |
| `nome` | String | Nome completo do aluno |
| `idade` | Integer | Idade do aluno |
| `peso` | Decimal | Peso do aluno |
| `tempo_pratica_meses` | Integer | Tempo de prática em meses |
| `nivel` | String | Nível calculado automaticamente |

> ⚠️ O campo `nivel` é **calculado automaticamente** com base no tempo de prática e **não deve ser enviado no payload**.

---

## 🔁 Regras de Negócio – Nível do Aluno

O nível do aluno é definido automaticamente conforme o tempo de prática:

- **Iniciante** → até X meses
- **Intermediário** → entre X e Y meses
- **Experiente** → acima de Y meses

Essa lógica está centralizada no **Serializer/Service**, garantindo consistência em toda a aplicação.

---

## 🌐 Rotas Disponíveis

Base URL:
/api/alunos/

bash
Copiar código

### ➕ Criar Aluno
**POST** `/api/alunos/`

**Payload de exemplo:**
```json
{
  "nome": "Aluno Miguel",
  "idade": 21,
  "peso": 70,
  "tempo_pratica_meses": 8
}
Resposta esperada:
201 Created

```

## 📄 Listar Alunos

**GET** `/api/alunos/`

Retorna a lista de todos os alunos cadastrados no sistema.

---

## 🔍 Detalhar Aluno

**GET** `/api/alunos/{id}/`

Retorna os dados de um aluno específico com base no seu identificador.

---

## ✏️ Atualizar Aluno

### Atualização completa
**PUT** `/api/alunos/{id}/`

Atualiza **todos os campos** do aluno.  
Requer o envio do objeto completo no payload.

---

### Atualização parcial
**PATCH** `/api/alunos/{id}/`

Atualiza **apenas os campos informados** no payload.

---

## 🗑️ Remover Aluno

**DELETE** `/api/alunos/{id}/`

Remove o aluno do sistema.

**Resposta esperada:**

---

## 🌐 Rotas de Treino


## ➕ Criar Treino para um Aluno

### 📍 Base URL
**POST** `/api/alunos/{id_aluno}/treinos/`

### Payload de exemplo
```json
{
  "aluno": 1,
  "nivel": "INICIANTE",
  "ativo": true
}

```

---

## 📄 Listar Treinos do Aluno

### 📍 Base URL

**GET** `/api/alunos/{id_aluno}/treinos/`


### Payload de exemplo
```json
{
  "message": "Treinos listados com sucesso",
  "data": [
    {
      "id": 2,
      "nivel": "",
      "ativo": true,
      "criado_em": "2026-01-19T02:58:38.180288Z",
      "exercicios": [
        {
          "treino": 2,
          "exercicio_id": 1,
          "dia": "A",
          "ordem": 1,
          "repeticoes": null,
          "series": null,
          "exercicio": {
            "external_id": "0009",
            "name": "assisted chest dip (kneeling)",
            "target": "chest",
            "difficulty": 1,
            "category": "strength",
            "body_part": "chest",
            "equipment": "leverage machine",
            "instructions": [
              "Adjust the machine to your desired height and secure your knees on the pad.",
              "Grasp the handles with your palms facing down and your arms fully extended.",
              "Lower your body by bending your elbows until your upper arms are parallel to the floor.",
              "Pause for a moment, then push yourself back up to the starting position."
            ]
          }
        }
      ]
    }
  ]
}

```
