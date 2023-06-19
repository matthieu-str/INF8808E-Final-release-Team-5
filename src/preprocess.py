def to_lowercase(df):
    # putting every str column in lowercase
    str_columns = ["nom", "prénom", "titre", "discipline", "domaine", "langue", "grade"]
    for col in str_columns:
        df[col] = df[col].str.lower()
    return df
