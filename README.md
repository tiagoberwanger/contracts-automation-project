# 📝 Automação de geração de contratos

Modelo de **contrato de locação** projetado para ser **simples, versionável e automatizável**.

Este repositório **não é um sistema completo**, mas sim a base contratual e lógica necessária para evoluir para automação.

## 📌 O que é este projeto?

Um **modelo único de contrato de locação** que suporta:

- Locatário **Pessoa Física ou Pessoa Jurídica**
- **Beneficiário** (ocupante residente) *OU*
- **Fiador** (garantia)

## 🧠 Conceito principal

O contrato usa **blocos condicionais** (marcadores técnicos) que:

- não aparecem no contrato final
- servem como referência para scripts ou LLMs
- permitem ativar ou remover trechos automaticamente

## Tecnologias

### Frontend

- Streamlit - criação facilitada de formulários

### Backend

- FastAPI - criação facilitada de uma API para geração de contratos

## Próximos passos

- Banco de dados para salvar histórico de contratos gerados
- Expandir com o uso de LLM para leitura de documentos e extração de dados, facilitando um pré-preenchimento dos dados de contrato
