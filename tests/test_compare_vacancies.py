from src.CompareVacancies import CompareVacancies


def test_generate_salary_dict_valid():
    v = CompareVacancies('python')

    assert isinstance(v.generate_salary_dict(), dict)
    assert len(v.generate_salary_dict()) > 0


def test_generate_salary_dict_some_choice():
    vacancy_1 = CompareVacancies('dsf')
    assert len(vacancy_1.generate_salary_dict()) == 0
    assert len(CompareVacancies(1).generate_salary_dict()) == 0
