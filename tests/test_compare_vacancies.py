from src.CompareVacancies import CompareVacancies


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
