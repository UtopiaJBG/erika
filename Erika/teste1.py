import streamlit as st
import pandas as pd
from datetime import datetime  # Import datetime module

def load_data():
    try:
        df = pd.read_csv("planilha.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Remedio", "Data de Validade", "Quantia"])
    return df

def save_data(df):
    df.to_csv("planilha.csv", index=False)

def get_current_date():
    return datetime.now().date()  # Get current date

def main():
    st.title("Gestão de Medicamentos")

    df = load_data()

    menu = ["Adicionar Medicamento", "Editar Medicamento", "Excluir Medicamento", "Visualizar Medicamentos"]
    choice = st.sidebar.selectbox("Selecione uma opção:", menu)

    if choice == "Adicionar Medicamento":
        st.header("Adicionar Medicamento")

        remedio = st.text_input("Nome do Medicamento:")
        # Use the get_current_date function to get the current date
        data_validade = st.date_input("Data de Validade:", value=get_current_date())
        quantia = st.number_input("Quantidade:", min_value=1, step=1)

        if st.button("Adicionar"):
            # Concatenate medication name and current date in the "Remedio" field
            remedio_com_data = f"{remedio} - {get_current_date()}"
            novo_dado = {"Remedio": remedio_com_data, "Data de Validade": data_validade, "Quantia": quantia}
            df = df.append(novo_dado, ignore_index=True)
            save_data(df)
            st.success("Medicamento adicionado com sucesso!")
    elif choice == "Editar Medicamento":
        st.header("Editar Medicamento")

        if st.checkbox("Mostrar Medicamentos"):
            st.write(df)

        busca_medicamento_editar = st.text_input("Digite o nome do medicamento que deseja editar:")
        medicamentos_filtrados_editar = df[df["Remedio"].str.contains(busca_medicamento_editar, case=False, na=False)]

        if not medicamentos_filtrados_editar.empty:
            st.write(medicamentos_filtrados_editar)
        else:
            st.warning("Nenhum medicamento encontrado com o nome digitado.")

        remedio_para_editar = st.selectbox("Escolha o medicamento para editar:", medicamentos_filtrados_editar["Remedio"].unique(), key="editar_medicamento")
        indice_para_editar = df[df["Remedio"] == remedio_para_editar].index

        if st.button("Mostrar Detalhes do Medicamento"):
            if not indice_para_editar.empty:
                detalhes = df.loc[indice_para_editar]
                st.write(detalhes)
            else:
                st.warning("Medicamento não encontrado. Certifique-se de escolher um medicamento válido.")

        quantidade_utilizada = st.number_input("Quantidade Utilizada:", min_value=0, step=1)

        if st.button("Atualizar Quantidade Utilizada"):
            if not indice_para_editar.empty:
                df.loc[indice_para_editar, "Quantia Utilizada"] += quantidade_utilizada
                df.loc[indice_para_editar, "Quantia"] -= quantidade_utilizada
                save_data(df)
                st.success(f"{quantidade_utilizada} unidades do medicamento foram utilizadas com sucesso!")
            else:
                st.warning("Medicamento não encontrado. Certifique-se de escolher um medicamento válido.")
    elif choice == "Visualizar Medicamentos":
        st.header("Visualizar Medicamentos")

        if not df.empty:
            st.write()
        else:
            st.warning("Nenhum medicamento cadastrado.")
            
        if not df.empty:
            # Adicione uma caixa de entrada de texto para buscar medicamentos enquanto o usuário digita
            busca_usuario = st.text_input("Digite o nome do medicamento para buscar:")
            medicamentos_filtrados = df[df["Remedio"].str.contains(busca_usuario, case=False, na=False)]

            st.write(medicamentos_filtrados)

            if medicamentos_filtrados.empty:
                st.warning("Nenhum medicamento encontrado com o nome digitado.")
        else:
            st.warning("Nenhum medicamento cadastrado.")

        # Filtrar Medicamentos por Data de Validade
        st.subheader("Filtrar Medicamentos por Data de Validade")
        data_inicio = st.date_input("Data Inicial:")
        data_fim = st.date_input("Data Final:")

        # Converter a coluna "Data de Validade" para datetime
        df["Data de Validade"] = pd.to_datetime(df["Data de Validade"])

        medicamentos_filtrados = df[(df["Data de Validade"] >= pd.Timestamp(data_inicio)) & (df["Data de Validade"] <= pd.Timestamp(data_fim))]
        st.write(medicamentos_filtrados)

    elif choice == "Excluir Medicamento":
        st.header("Excluir Medicamento")

        if st.checkbox("Mostrar Medicamentos"):
            st.write(df)

        # Adicione um botão para excluir todos os medicamentos com quantidade zero
        if st.button("Excluir Medicamentos com Quantidade 0"):
            df = df[df["Quantia"] > 0]
            save_data(df)
            st.success("Medicamentos com quantidade zero foram excluídos com sucesso!")

        remedio_para_excluir = st.text_input("Digite o nome do medicamento que deseja excluir:")

        if st.button("Excluir Medicamento"):
            df = df[df["Remedio"] != remedio_para_excluir]
            save_data(df)
            st.success("Medicamento excluído com sucesso!")

if __name__ == "__main__":
    main()

