from pydantic import BaseModel
from typing import List, Optional


class ItemVistoria(BaseModel):
    item_descricao_estado: str


class ContratoInput(BaseModel):
    # --- Dados do Locatário ---
    nome_locatario: str
    eh_pj: bool
    cpf_cnpj_locatario: str
    endereco_locatario: str

    # --- Lógica de Garantia/Residência ---
    tem_beneficiario: bool = False
    nome_beneficiario: Optional[str] = None
    estado_civil_beneficiario: Optional[str] = None
    cpf_beneficiario: Optional[str] = None
    endereco_beneficiario: Optional[str] = None

    tem_fiador: bool = False
    nome_fiador: Optional[str] = None
    estado_civil_fiador: Optional[str] = None
    profissao_fiador: Optional[str] = None
    cpf_fiador: Optional[str] = None
    endereco_fiador: Optional[str] = None

    # --- Objeto e Vigência ---
    identificacao_unidade: str
    prazo_contratual: int
    data_inicial: str
    data_final: str

    # --- Valores Financeiros ---
    valor_aluguel: str
    dia_vencimento: int
    valor_pintura: str

    # --- Vistoria (Anexo I) ---
    data_vistoria: str
    itens_moveis: List[ItemVistoria] = []
    descricao_paredes: str
    descricao_tetos: str
    descricao_pisos: str
    descricao_portas: str
    descricao_janelas: str
    descricao_instalacoes_eletricas: str
    descricao_instalacoes_hidraulicas: str
    observacoes_vistoria: Optional[str] = 'Nenhuma observação'

    # --- Rodapé ---
    data_assinatura: str
