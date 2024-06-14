def get_vacancies_list(vacancies: list) -> list or None:
    """ Check vacancies list is None"""
    return vacancies if vacancies is not None else 'I dont found vacancies for you'
