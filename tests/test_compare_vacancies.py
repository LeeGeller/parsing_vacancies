from src.CompareVacancies import CompareVacancies
from copy import deepcopy


def test_generate_salary_dict_valid():
    v = CompareVacancies('python')

    assert isinstance(v.generate_salary_dict(), dict)
    assert len(v.generate_salary_dict()) > 0


def test_generate_salary_dict_some_choice():
    vacancy_1 = CompareVacancies('dsf')
    assert len(vacancy_1.generate_salary_dict()) == 0
    assert len(CompareVacancies(1).generate_salary_dict()) == 0


def test_get_vacancies_check_salary():
    vacancy = CompareVacancies('python')
    vacancy.get_vacancies()

    assert 'from_None' in vacancy.salary_all.keys()
    assert 80000 in vacancy.salary_all.keys()

    vacancy_2 = CompareVacancies('python', 80000)
    check_list = []
    for value in vacancy_2.get_vacancies():
        for key, val in value.items():
            if value['salary']['from'] == None:
                check_list.append(val)

    assert len(check_list) == 0


def test_get_vacancies_len_is_zero():
    vacancy_1 = CompareVacancies('tttttttt', 300000)
    vacancy_1.get_vacancies()
    assert len(vacancy_1.salary_all) < 2
    assert vacancy_1.message == "Vacancy not found"


def test_get_top_vacancies():
    vacancy_1 = CompareVacancies('python', 50000)

    assert len(vacancy_1.get_top_vacancies()) > 0
    top_list = []
    for keys in vacancy_1.salary_top.keys():
        top_list.append(keys)
    new_list = deepcopy(top_list)

    assert sorted(top_list, reverse=True) == new_list