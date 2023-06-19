def to_lowercase(df):
    # putting every str column in lowercase
    str_columns = ["nom", "prénom", "titre", "discipline", "domaine", "langue", "grade"]
    for col in str_columns:
        df[col] = df[col].str.lower()
    return df
def delete_unecessary_columns(df):
    df = df.drop(columns=['titre', 'nom','prénom','url','source'])
    return df

def assign_and_range_pages(df):
    def assign_page_range(pages):
        if pages > 0 and pages <= 100:
            return '[0-100]'
        elif pages <= 250:
            return '[101-250]'
        elif pages <= 500:
            return '[251-500]'
        elif pages <= 2035:
            return '[501-2035]'
        else: 
            return '0'
    
    df['range of pages'] = df['pages'].apply(assign_page_range)
    return df

def delete_duplicate_disciplines(df):
    # Create a dictionary to store the disciplines and their corresponding domains
    discipline_domains = {}
    idx1= df.columns.get_loc('discipline')
    idx2= df.columns.get_loc('domaine')
    # Iterate over each row in the table
    for index, row in df.iterrows():
        discipline = row[idx1]  # Assuming discipline is in the column (index 1)
        domaine = row[idx2]  # Assuming domaine is in the column (index 2)

        # Check if the discipline already exists in the dictionary
        if discipline in discipline_domains:
            # If the discipline exists, check if the current domain is the same
            # If not, remove the row from the table
            if discipline_domains[discipline] != domaine:
                df = df.drop(index)
        else:
            # If the discipline doesn't exist, add it to the dictionary
            discipline_domains[discipline] = domaine

    return df
