# import pandas as pd
# import streamlit as st
# from datetime import datetime
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# st.set_page_config(page_title="Chamados da Manutenção", page_icon="🛠️")

# st.title("🛠️ Chamados da Manutenção")


# def enviar_mensagem(destinatario, assunto, mensagem):
#     remetente = "luiz.silva@cidadania4u.com.br"
#     senha = st.secrets["LuizFe80"]
#     msg = MIMEMultipart()
#     msg["From"] = remetente
#     msg["To"] = destinatario
#     msg["Subject"] = assunto
#     msg.attach(MIMEText(mensagem, 'plain'))
#     try:
#         server = smtplib.SMTP('smtp.office365.com', 587)
#         server.starttls()
#         server.login(remetente, senha)
#         server.sendmail(remetente, destinatario, msg.as_string())
#         server.quit()
#         st.success("✅ E-mail enviado com sucesso!")
#     except Exception as e:
#         st.error(f"❌ Falha ao enviar e-mail: {e}")

# form = st.form(key='manutencao_form')
# with form:
#     data = st.date_input("Data do chamado", value=datetime.now())
#     andar = st.selectbox("Andar",["3° Andar","4° Andar"])
#     sala = st.selectbox("Sala",["backoffice",
#                          "Banheiro",
#                          "Comercial",
#                          "Copa",
#                          "Recepção",
#                          "Reunião"
#                          "Sala Portugal",
#                          "Sala Itália",
#                          "Sala Espanha",
#                          "Sala 1",
#                          "Sala 2",
#                          "Sala 3",
#                          "Sala 4",
#                          "Sala BeCivis",
#                          "Financeiro",
#                          "Arquivo",
#                          "GG",
#                          "Game4u"])
    
#     descricao = st.text_area("Descrição do problema", height=150)

#     botao = st.form_submit_button("Enviar chamado")

# if botao:
#     novo_chamado = pd.DataFrame({
#         "Data": [data],
#         "Andar": [andar],
#         "Sala": [sala],
#         "Descrição": [descricao]
#     })
    
#     try:
#         df_chamados = pd.read_excel("chamados_manutencao.xlsx")
#         df_chamados = pd.concat([df_chamados, novo_chamado], ignore_index=True)
#     except FileNotFoundError:
#         df_chamados = novo_chamado
    
#     df_chamados.to_excel("chamados_manutencao.xlsx", index=False)
    
#     st.success("✅ Chamado enviado com sucesso!")
#     st.dataframe(df_chamados)




# import smtplib
# from email.mime.text import MimeText
# from email.mime.multipart import MimeMultipart
# import streamlit as st

# def enviar_email(destinatario, assunto, mensagem):
#     # Configurações do email (coloque em variáveis de ambiente)
#     remetente = "luiz.silva@cidadania4u.com.br"
#     senha = st.secrets["LuizFe80"]  # Recomendado usar secrets
    
#     # Criando email
#     msg = MimeMultipart()
#     msg['From'] = remetente
#     msg['To'] = destinatario
#     msg['Subject'] = assunto
    
#     msg.attach(MimeText(mensagem, 'plain'))
    
#     try:
#         # Conectando ao servidor SMTP
#         server = smtplib.SMTP('smtp.office365.com', 587)
#         server.starttls()
#         server.login(remetente, senha)
#         text = msg.as_string()
#         server.sendmail(remetente, destinatario, text)
#         server.quit()
#         return True
#     except Exception as e:
#         st.error(f"Erro ao enviar email: {e}")
#         return False
    
# def main():
#     st.title("Sistema de Chamados")
    
#     with st.form("chamado_form"):
#         nome = st.text_input("Nome")
#         email = st.text_input("Email")
#         problema = st.text_area("Descreva o problema")
#         enviar = st.form_submit_button("Enviar Chamado")
        
#         if enviar:
#             # Mensagem personalizada
#             mensagem_email = f"""
#             Olá {nome}!
            
#             Recebemos seu chamado:
#             {problema}
            
#             Número do chamado: #001
#             Em breve entraremos em contato.
            
#             Atenciosamente,
#             Equipe de Suporte
#             """
            
#             # Enviar email
#             if enviar_email(email, "Confirmação de Chamado", mensagem_email):
#                 st.success("Chamado enviado e email de confirmação disparado!")


# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# meu_email = "luiz.silva@cidadania4u.com.br"
# minha_senha = "LuizFe80"
# destinatarios = ["lair.campos@cidadania4u.com.br",""]

# def enviar_email(dados_chamados):
#     try:
#         msg = MIMEMultipart()
#         msg["From"] = meu_email
#         msg["To"] = ", ".join(destinatarios)
#         msg["Subject"] = f"🚨Chamado Manutenção🚨 - {dados_chamados['andar']} - {dados_chamados['sala']}"

#         corpo = f"""
#             Novo Chamado de Manutenção
            
#             Data: {dados_chamados['data']}
#             Andar: {dados_chamados['andar']}
#             Sala: {dados_chamados['sala']}

#             Problema:
#             {dados_chamados['problema']}
#         """
#         msg.attach(MIMEText(corpo,"plain"))

#         server = smtplib.SMTP('smtp.office365.com', 587)
#         server.starttls()
#         server.login(meu_email, minha_senha)
#         server.send_message(msg)
#         server.quit()

#         return True
#     except Exception as e:
#         st.error(f"Erro ao enviar email: {e}")
#         return False
    

# def main():
#     st.set_page_config(page_title="Chamados da Manutenção")

#     st.title("Chamados para a manutenção")
#     st.markdown("-------")

#     with st.form("chamado_form"):

#         st.subheader("Abrir Chamado")
        
#         data = datetime.now().strftime("%d/%m/%Y %H:%M")
#         st.info(f"📅 Data: {data}")

#         col1, col2 = st.columns(2)

#         with col1:

#             andar = st.selectbox("Andar",["3° Andar","4° Andar"])
#         with col2:
#             sala = st.selectbox("Sala",["backoffice",
#                          "Banheiro",
#                          "Comercial",
#                          "Copa",
#                          "Recepção",
#                          "Reunião",
#                          "Sala Portugal",
#                          "Sala Itália",
#                          "Sala Espanha",
#                          "Sala 1",
#                          "Sala 2",
#                          "Sala 3",
#                          "Sala 4",
#                          "Sala BeCivis",
#                          "Financeiro",
#                          "Arquivo",
#                          "GG",
#                          "Game4u"])
        
#         descricao = st.text_area("Descrição do Problema", placeholder="Descreva o que problema em poucas palavras")

#         button = st.form_submit_button("Enviar Chamado")

#         if button:
#             if not descricao:
#                 st.error(" Por Favor, descreva o problema")
#             else:

#                 chamado = {
#                     "data": data,
#                     "andar": andar,
#                     "sala": sala,
#                     "descricao": descricao
#                 }

#                 if enviar_email(chamado):
#                     st.success(" Chamado enviado!")
#                     st.balloons()

#                     #Resumo do Chamado
#                     st.subheader(" Resumo do Chamado")
#                     st.write(f"**Data**: {chamado['data']}")
#                     st.write(f"**Local:** {chamado['andar']} - {chamado['sala']}")
#                     st.write(f"**Problema**: {chamado['descricao']}")

#                 else:
#                     st.error("Erro ao enviar o chamado. Tente Novamente")

# if __name__ == "__main__":
#     main()


# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# meu_email = "felipe32br@gmail.com"
# minha_senha = "Felipe32br@#$%SiRo8*"
# destinatarios = ["luizzz08totop@gmail.com","luiz.silva@cidadania4u.com.br"]

# def enviar_email(dados_chamados):
#     try:
#         msg = MIMEMultipart()
#         msg["From"] = ""  # Use um Gmail
#         msg["To"] = ", ".join(destinatarios)
#         msg["Subject"] = f"🚨Chamado Manutenção🚨 - {dados_chamados['andar']} - {dados_chamados['sala']}"

#         corpo = f"""
# Novo Chamado de Manutenção

# Data: {dados_chamados['data']}
# Andar: {dados_chamados['andar']}
# Sala: {dados_chamados['sala']}

# Problema:
# {dados_chamados['descricao']}
#         """
#         msg.attach(MIMEText(corpo, "plain"))

#         # Configurações Gmail
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(meu_email, minha_senha)  # Use senha de app
#         server.send_message(msg)
#         server.quit()

#         return True
#     except Exception as e:
#         st.error(f"Erro ao enviar email: {e}")
#         return False
    

# def main():
#     st.set_page_config(page_title="Chamados da Manutenção")

#     st.title("Chamados para a manutenção")
#     st.markdown("-------")

#     with st.form("chamado_form"):
#         st.subheader("Abrir Chamado")
        
#         data = datetime.now().strftime("%d/%m/%Y %H:%M")
#         st.info(f"📅 Data: {data}")

#         col1, col2 = st.columns(2)

#         with col1:
#             andar = st.selectbox("Andar", ["3° Andar", "4° Andar"])

#         with col2:
#             sala = st.selectbox("Sala", [
#                 "backoffice",
#                 "Banheiro",
#                 "Comercial",
#                 "Copa",
#                 "Recepção",
#                 "Reunião",
#                 "Sala Portugal",
#                 "Sala Itália",
#                 "Sala Espanha",
#                 "Sala 1",
#                 "Sala 2",
#                 "Sala 3",
#                 "Sala 4",
#                 "Sala BeCivis",
#                 "Financeiro",
#                 "Arquivo",
#                 "GG",
#                 "Game4u"
#             ])
        
#         descricao = st.text_area("Descrição do Problema", placeholder="Descreva o problema em poucas palavras")

#         button = st.form_submit_button("Enviar Chamado")

#         if button:
#             if not descricao:
#                 st.error("Por favor, descreva o problema")
#             else:
#                 chamado = {
#                     "data": data,
#                     "andar": andar,
#                     "sala": sala,
#                     "descricao": descricao
#                 }

#                 if enviar_email(chamado):
#                     st.success("Chamado enviado!")
#                     st.balloons()

#                     # Resumo do Chamado
#                     st.subheader("Resumo do Chamado")
#                     st.write(f"**Data**: {chamado['data']}")
#                     st.write(f"**Local:** {chamado['andar']} - {chamado['sala']}")
#                     st.write(f"**Problema**: {chamado['descricao']}")
#                 else:
#                     st.error("Erro ao enviar o chamado. Tente Novamente")

# if __name__ == "__main__":
#     main()

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