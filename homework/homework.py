"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerles un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cambiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    import pandas as pd
    import zipfile
    import os
    import glob
    input_folder = "files/input/"
    output_folder = "files/output/"

    os.makedirs(output_folder, exist_ok=True)

    # Buscar archivos CSV dentro de archivos ZIP
    zip_files = glob.glob(os.path.join(input_folder, "*.zip"))

    # Lista para almacenar los DataFrames
    dataframes = []

    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, "r") as z:
            for file_name in z.namelist():
                if file_name.endswith(".csv"):
                    with z.open(file_name) as f:
                        df = pd.read_csv(f, sep=",", encoding="utf-8")
                        dataframes.append(df)

    # Concatenar todos los DataFrames
    df = pd.concat(dataframes, ignore_index=True)

    # Crear client.csv
    df_client = df[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]].copy()
    df_client["job"] = df_client["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    df_client["education"] = df_client["education"].str.replace(".", "_", regex=False).replace("unknown", pd.NA)
    df_client["credit_default"] = df_client["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    df_client["mortgage"] = df_client["mortgage"].apply(lambda x: 1 if x == "yes" else 0)
    df_client.to_csv(os.path.join(output_folder, "client.csv"), index=False, encoding="utf-8")

    # Crear campaign.csv
    df_campaign = df[[
        "client_id", "number_contacts", "contact_duration", 
        "previous_campaign_contacts", "previous_outcome", "campaign_outcome", "day", "month"
    ]].copy()

    df_campaign["previous_outcome"] = df_campaign["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    df_campaign["campaign_outcome"] = df_campaign["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)
    df_campaign["last_contact_date"] = pd.to_datetime(df_campaign["day"].astype(str) + "-" + df_campaign["month"] + "-2022", format="%d-%b-%Y")

    df_campaign = df_campaign.drop(columns=["day", "month"])
    df_campaign.to_csv(os.path.join(output_folder, "campaign.csv"), index=False, encoding="utf-8")

    # Crear economics.csv
    df_economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()
    df_economics.to_csv(os.path.join(output_folder, "economics.csv"), index=False, encoding="utf-8")

if __name__ == "__main__":
    clean_campaign_data()

