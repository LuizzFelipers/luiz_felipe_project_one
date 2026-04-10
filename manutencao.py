import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure com SEUS dados do Gmail
meu_email_gmail = "felipers3233@gmail.com"  # Seu email Gmail
minha_senha_app = "gknw imvj iotk seao"  # A senha de 16 caracteres que você gerou
destinatarios = ["luiz.silva@cidadania4u.com.br","luizzz08totop@gmail.com"]

def enviar_email_gmail(dados_chamados):
    try:
        msg = MIMEMultipart()
        msg["From"] = meu_email_gmail
        msg["To"] = ", ".join(destinatarios)
        msg["Subject"] = f"🚨Chamado Manutenção🚨 - {dados_chamados['andar']} - {dados_chamados['sala']}"

        corpo = f"""
Novo Chamado de Manutenção

Data: {dados_chamados['data']}
Andar: {dados_chamados['andar']}
Sala: {dados_chamados['sala']}

Problema:
{dados_chamados['descricao']}
        """
        msg.attach(MIMEText(corpo, "plain"))

        # Configurações Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(meu_email_gmail, minha_senha_app)  # Use a senha de aplicativo aqui
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        st.error(f"Erro ao enviar email: {e}")
        return False

def main():
    st.set_page_config(page_title="Chamados da Manutenção")

    st.title("Chamados para a manutenção")
    st.markdown("-------")

    with st.form("chamado_form"):
        st.subheader("Abrir Chamado")
        
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        st.info(f"📅 Data: {data}")

        col1, col2 = st.columns(2)

        with col1:
            andar = st.selectbox("Andar", ["3° Andar", "4° Andar"])

        with col2:
            sala = st.selectbox("Sala", [
                "backoffice", "Banheiro", "Comercial", "Copa", "Recepção", "Reunião",
                "Sala Portugal", "Sala Itália", "Sala Espanha", "Sala 1", "Sala 2",
                "Sala 3", "Sala 4", "Sala BeCivis", "Financeiro", "Arquivo", "GG", "Game4u"
            ])
        
        descricao = st.text_area("Descrição do Problema", placeholder="Descreva o problema em poucas palavras")

        button = st.form_submit_button("Enviar Chamado")

        if button:
            if not descricao:
                st.error("Por favor, descreva o problema")
            else:
                chamado = {
                    "data": data,
                    "andar": andar,
                    "sala": sala,
                    "descricao": descricao
                }

                if enviar_email_gmail(chamado):
                    st.success("Chamado enviado!")
                    st.balloons()

                    st.subheader("Resumo do Chamado")
                    st.write(f"**Data**: {chamado['data']}")
                    st.write(f"**Local:** {chamado['andar']} - {chamado['sala']}")
                    st.write(f"**Problema**: {chamado['descricao']}")
                else:
                    st.error("Erro ao enviar o chamado. Tente Novamente")

if __name__ == "__main__":
    main()
