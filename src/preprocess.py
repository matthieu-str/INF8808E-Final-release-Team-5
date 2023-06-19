import pandas as pd
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

def other_languages(df_count, year_min, year_max):
    '''
    This function is gathering all the other languages than English and French into an "other" category
    :param df_count: input dataframe grouped by languages
    :param year_min: minimum year for gathering
    :param year_max: maximum year for gathering
    :return: processed dataframe
    '''
    langues_other = ["de", "es", "it", "pt"]
    pattern_langues_other = '|'.join(langues_other)
    res = []

    for year in range(year_min, year_max + 1):
        total_other = df_count[(df_count["année"] == year) & (
            df_count["langue"].str.contains(pattern_langues_other))]["count"].sum()
        res.append([year, "other", total_other])

    df_other = pd.DataFrame(res, columns=["année", "langue", "count"])

    df_count = df_count.drop(
        df_count[df_count.langue.str.contains(pattern_langues_other)].index)
    df_count = pd.concat([df_count, df_other])

    df_count.sort_values(by=["année"], ignore_index=True, inplace=True)

    return df_count