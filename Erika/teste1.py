import streamlit as st
import pandas as pd

def load_data():
    try:
        df = pd.read_csv("planilha.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Remedio", "Data de Validade", "Quantia"])
    return df

def save_data(df):
    df.to_csv("planilha.csv", index=False)
    
    
def main():
    st.title("Gestão de Medicamentos")

    df = load_data()

    menu = ["Adicionar Medicamento", "Editar Medicamento", "Excluir Medicamento", "Visualizar Medicamentos"]
    choice = st.sidebar.selectbox("Selecione uma opção:", menu)

    if choice == "Adicionar Medicamento":
        st.header("Adicionar Medicamento")

        remedio = st.text_input("Nome do Medicamento:")
        data_validade = st.date_input("Data de Validade:")
        quantia = st.number_input("Quantidade:", min_value=1, step=1)

        if st.button("Adicionar"):
            novo_dado = {"Remedio": remedio, "Data de Validade": data_validade, "Quantia": quantia}
            df = df.append(novo_dado, ignore_index=True)
            save_data(df)
            st.success("Medicamento adicionado com sucesso!")

    elif choice == "Editar Medicamento":
        st.header("Editar Medicamento")

        if st.checkbox("Mostrar Medicamentos"):
            st.write(df)

        remedio_para_editar = st.text_input("Digite o nome do medicamento que deseja editar com sua data de fabricação/validade:")
        indice_para_editar = df[df["Remedio"] == remedio_para_editar].index

        if st.button("Mostrar Detalhes do Medicamento"):
            if not indice_para_editar.empty:
                detalhes = df.loc[indice_para_editar]
                st.write(detalhes)
            else:
                st.warning("Medicamento não encontrado. Certifique-se de digitar o nome corretamente.")

        novo_quantia = st.number_input("Nova Quantidade:", min_value=0, step=1)

        if st.button("Atualizar Quantidade"):
            if not indice_para_editar.empty:
                df.loc[indice_para_editar, "Quantia"] = novo_quantia
                save_data(df)
                st.success("Quantidade atualizada com sucesso!")
            else:
                st.warning("Medicamento não encontrado. Certifique-se de digitar o nome corretamente.")

    elif choice == "Visualizar Medicamentos":
        st.header("Visualizar Medicamentos")

        if not df.empty:
            st.write(df)
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

        remedio_para_excluir = st.text_input("Digite o nome do medicamento que deseja excluir:")
        if st.button("Excluir"):
            df = df[df["Remedio"] != remedio_para_excluir]
            save_data(df)
            st.success("Medicamento excluído com sucesso!")




if __name__ == "__main__":
    main()

