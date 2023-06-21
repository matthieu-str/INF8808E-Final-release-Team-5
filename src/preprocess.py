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

def other_languages(df_count):
    '''
    This function is gathering all the other languages than English and French into an "other" category
    :param df_count: input dataframe grouped by languages
    :return: processed dataframe
    '''
    langues_other = ["de", "es", "it", "pt"]
    pattern_langues_other = '|'.join(langues_other)
    res = []
    year_min = df_count["année"].min()
    year_max = df_count["année"].max()

    for year in range(year_min, year_max + 1):
        total_other = df_count[(df_count["année"] == year) & (
            df_count["langue"].str.contains(pattern_langues_other))]["count"].sum()
        res.append([year, "autres", total_other])

    df_other = pd.DataFrame(res, columns=["année", "langue", "count"])

    df_count = df_count.drop(
        df_count[df_count.langue.str.contains(pattern_langues_other)].index)
    df_count = pd.concat([df_count, df_other])

    df_count.sort_values(by=["année"], ignore_index=True, inplace=True)

    return df_count

def get_top_univ(df_count, n):
    '''
    Returns a list of the top 10 universities un terms of cumulated number of publications
    :param df_count: grouped by dataframe
    :param n: number of top to keep
    :return: list of str containing top 10 university names
    '''
    return list(df_count.groupby(by=['univ'], as_index=False).sum('count')[['univ', 'count']].sort_values(by='count', ascending=False).head(n)['univ'])

def other_univ(df_count):
    '''
    Only keeps the top 10 universities and replace all other by an "other" category
    :param df_count: the grouped by dataframe
    :return: the processed dataframe
    '''
    top_univ = get_top_univ(df_count, 5)
    not_top_univ = list(set(list(df_count.univ.unique())) - set(top_univ))
    pattern_univ_other = '|'.join(not_top_univ)
    res = []
    year_min = df_count["année"].min()
    year_max = df_count["année"].max()

    for year in range(year_min, year_max + 1):
        total_other = df_count[(df_count["année"] == year) & (
            df_count["univ"].str.contains(pattern_univ_other))]["count"].sum()
        res.append([year, "Autres", total_other])

    df_other = pd.DataFrame(res, columns=["année", "univ", "count"])

    df_count = df_count.drop(
        df_count[df_count.univ.str.contains(pattern_univ_other)].index)
    df_count = pd.concat([df_count, df_other])

    df_count.sort_values(by=["année"], ignore_index=True, inplace=True)

    return df_count

def rename_languages(df_count):
    '''
    Rename languages for better readability
    :param df_count: grouped by dataframe
    :return: processed dataframe
    '''
    df_count.langue.replace(to_replace='fr', value='français', inplace=True)
    df_count.langue.replace(to_replace='en', value='anglais', inplace=True)
    return df_count

def rename_inclassable(df_count):
    df_count.domaine.replace(to_replace='inclassable',
                             value='programme individualisé ou inconnu',
                             inplace=True)
    return df_count

