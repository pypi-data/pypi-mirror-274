comma_separate = lambda x: ', '.join(x)
set_values_by = lambda x: f"SET { comma_separate([f'{i} = :{i}' for i in x]) }"
enumerate_values_by = lambda x: f"({ comma_separate(x) }) VALUES ({ comma_separate([f':{i}' for i in x]) })"


DIRECTIVES = {
    'set_values_by': set_values_by,
    'enumerate_values_by': enumerate_values_by,
}
