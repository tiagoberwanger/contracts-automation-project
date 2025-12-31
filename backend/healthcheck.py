from http import HTTPStatus

import requests
import streamlit as st

from frontend.app import API_URL


def check_server_status():
    if "server_ready" not in st.session_state:
        st.session_state.server_ready = False

    if not st.session_state.server_ready:
        placeholder = st.empty()
        placeholder.caption("⏳ Conectando ao servidor...")

        try:
            url_health = API_URL.replace('/gerar-contrato', '/health')
            response = requests.get(url_health, timeout=2)

            if response.status_code == HTTPStatus.OK:
                st.session_state.server_ready = True
                placeholder.caption("✅ Servidor Pronto")
        except:
            pass
    else:
        st.caption("✅ Servidor Pronto")
