'''
Transformation of letter to text. See constraints check in, in database script.
'''
def transform_type(text):
    try:
        dict = {'T' : 'Theory', 'E' : 'Experiment'}
        return dict[text]
    except:
        return result_uknown()

def transform_anisotropy_energy_type(text):
    try:
        dict = { 'U' : 'Uniaxial', 'C': 'Cubic', 'P' : 'Planar'}
        return dict[text]
    except:
        return result_uknown()

def transform_kind_of_anisotropy(text):
    try:
        dict = {'A': 'Easy axis', 'P': 'Planar easy axis', 'C': 'Easy cone'}
        return dict[text]
    except:
        return result_uknown()

def result_uknown():
    return 'None'

def unit_translate(value, unit):
    if value == None:
        return 'None'
    else:
        return str(value) + ' (' + unit + ')'

if __name__ == '__main__':
    object = ' '
    print(unit_translate(object,'texto'))