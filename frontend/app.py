from http import HTTPStatus

import streamlit as st
import requests
from datetime import date, timedelta

from backend.healthcheck import check_server_status

# Configuração da página para parecer um App de telemóvel
st.set_page_config(page_title="Contratos", page_icon="🏠")

st.title("Novo Contrato")

check_server_status()
# URL do seu backend (ajuste se estiver na nuvem)
API_URL = "https://contracts-automation-backend.onrender.com/gerar-contrato"

# Organização por abas para não sobrecarregar a tela do telemóvel
tab1, tab2, tab3, tab4 = st.tabs(["👤 Locatário", "🛡️ Garantia", "🏠 Imóvel", "📋 Vistoria"])

with tab1:
    locatario_nome = st.text_input("Nome do Locatário")
    eh_pessoa_juridica = st.radio("É pessoa jurídica?", ["não", "sim"], index=0)
    eh_pj = True if eh_pessoa_juridica == "sim" else False
    locatario_documento = st.text_input("CNPJ" if eh_pj else "CPF")
    locatario_endereco = st.text_input("Endereço do Locatário")

    if eh_pj:
        beneficiario_nome = st.text_input("Nome (Beneficiário)")
        beneficiario_estado_civil = st.text_input("Estado Civil (Beneficiário)")
        beneficiario_documento = st.text_input("CPF (Beneficiário)")
        beneficiario_endereco = st.text_input("Endereço (Beneficiário)")

with tab2:
    garantia = st.radio("Tipo de Garantia", ["Nenhuma", "Fiador"])

    tem_fiador = (garantia == "Fiador")
    if tem_fiador:
        fiador_nome = st.text_input("Nome do Fiador")
        fiador_estado_civil = st.text_input("Estado Civil (Fiador)")
        fiador_profissao = st.text_input("Profissão (Fiador)")
        fiador_documento = st.text_input("CPF (Fiador)")
        fiador_endereco = st.text_input("Endereço (Fiador)")

with tab3:
    unidade = st.text_input("Identificação da Unidade (ex: Apto 101)")
    prazo = st.number_input("Prazo (meses)", value=12)
    col1, col2 = st.columns(2)
    data_inicio = col1.date_input("Início", date.today())
    data_fim = col2.date_input("Fim", date.today() + timedelta(days=365))

    valor_aluguel = st.text_input("Valor Aluguel (ex: 1.200,00)")
    vencimento = st.slider("Dia de Vencimento", 1, 20, 5)
    valor_pintura = st.text_input("Valor Pintura (Cláusula 13ª)", value="200,00")

with tab4:
    data_vistoria = st.date_input("Data da Vistoria", date.today())
    paredes = st.text_area("Paredes", "Pintura nova, cor neutra, sem manchas.")
    tetos = st.text_area("Tetos", "Pintura nova, sem infiltrações.")
    pisos = st.text_area("Pisos", "Rejuntes e pisos limpos e sem riscos ou manchas.")
    portas = st.text_area("Portas", "Em perfeito estado, sem riscos ou rachados.")
    janelas = st.text_area("Janelas", "Vidros íntegros e limpos.")
    instalacoes_eletricas = st.text_area("Instalações elétricas", "Funcionando corretamente.")
    instalacoes_hidraulicas = st.text_area("Instalações hidráulicas", "Sem vazamentos.")

    st.write("---")
    st.subheader("Móveis e Eletros (Anexo I)")

    if 'itens_vistoria' not in st.session_state:
        st.session_state.itens_vistoria = [""]

    def adicionar_item():
        st.session_state.itens_vistoria.append("")

    for i, valor in enumerate(st.session_state.itens_vistoria):
        col_input, col_btn = st.columns([0.85, 0.15])

        st.session_state.itens_vistoria[i] = col_input.text_input(
            f"Item {i + 1}",
            value=valor,
            key=f"item_input_{i}",
            label_visibility="collapsed"
        )

        if col_btn.button("🗑️", key=f"btn_remove_{i}"):
            st.session_state.itens_vistoria.pop(i)
            st.rerun()

    st.button("➕ Adicionar outro item", on_click=adicionar_item)

    itens = [{"item_descricao_estado": txt} for txt in st.session_state.itens_vistoria if txt.strip() != ""]

if st.button("GERAR CONTRATO", use_container_width=True):
    payload = {
        "nome_locatario": locatario_nome,
        "eh_pj": eh_pj,
        "cpf_cnpj_locatario": locatario_documento,
        "endereco_locatario": locatario_endereco,
        "nome_beneficiario": beneficiario_nome if eh_pj else None,
        "estado_civil_beneficiario": beneficiario_estado_civil if eh_pj else None,
        "cpf_beneficiario": beneficiario_documento if eh_pj else None,
        "endereco_beneficiario": beneficiario_endereco if eh_pj else None,
        "tem_fiador": tem_fiador,
        "nome_fiador": fiador_nome if tem_fiador else None,
        "estado_civil_fiador": fiador_estado_civil if tem_fiador else None,
        "profissao_fiador": fiador_profissao if tem_fiador else None,
        "cpf_fiador": fiador_documento if tem_fiador else None,
        "endereco_fiador": fiador_endereco if tem_fiador else None,
        "identificacao_unidade": unidade,
        "prazo_contratual": prazo,
        "data_inicial": data_inicio.strftime("%d/%m/%Y"),
        "data_final": data_fim.strftime("%d/%m/%Y"),
        "valor_aluguel": valor_aluguel,
        "dia_vencimento": vencimento,
        "valor_pintura": valor_pintura,
        "data_vistoria": data_vistoria.strftime("%d/%m/%Y"),
        "itens_moveis": itens,
        "descricao_paredes": paredes,
        "descricao_tetos": tetos,
        "descricao_pisos": pisos,
        "descricao_portas": portas,
        "descricao_janelas": janelas,
        "descricao_instalacoes_eletricas": instalacoes_eletricas,
        "descricao_instalacoes_hidraulicas": instalacoes_hidraulicas,
        "data_assinatura": date.today().strftime("%d/%m/%Y")
    }

    with st.spinner("⏳ Gerando o contrato..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=90)
            if response.status_code == HTTPStatus.OK:
                st.success("✅ Contrato gerado com sucesso!")
                st.download_button(
                    label="⬇️Baixar contrato (.docx)",
                    data=response.content,
                    file_name=f"contrato_{locatario_nome.replace(" ", "_")}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            else:
                st.error(f"❌ Erro no servidor: {response.text}")
        except Exception as e:
            st.error(f"Não foi possível conectar ao Backend: {e}")
