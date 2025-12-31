import os

from io import BytesIO
from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from docxtpl import DocxTemplate
from starlette.middleware.cors import CORSMiddleware

from backend.schemas import ContratoInput

app = FastAPI(title="Gerador de Contratos Condomínio")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://contrato-condominioberwanger.streamlit.app/"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "v1", "modelo_contrato.docx")

@app.post("/gerar-contrato")
async def gerar_contrato(dados: ContratoInput):
    """
    Recebe os dados do formulário, preenche o template Word e retorna o arquivo para download.
    """
    try:
        # 1. Verifica se o ficheiro de modelo existe
        if not os.path.exists(TEMPLATE_PATH):
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Template de contrato não encontrado.")

        # 2. Carrega o modelo em docxtpl
        doc = DocxTemplate(TEMPLATE_PATH)

        # 3. Convertemos o objeto Pydantic num dicionário Python
        contexto = dados.model_dump()

        # 4. Renderiza o contrato
        doc.render(contexto)

        # 5. Salva o resultado num buffer de memória
        target_stream = BytesIO()
        doc.save(target_stream)
        target_stream.seek(0) # Volta ao início do ficheiro para leitura

        # 6. Define o nome do ficheiro de saída
        nome_arquivo = f"contrato_{dados.nome_locatario.replace(' ', '_')}.docx"

        # 7. Retorna o ficheiro como um stream para o navegador
        return StreamingResponse(
            target_stream,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={nome_arquivo}"}
        )

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Erro ao gerar contrato: {str(e)}")
