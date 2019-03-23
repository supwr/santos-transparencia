import os
from settings import LOCACOES_PATH, CONTRATOS_PATH, CONVENIOS_PATH, DB_PATH


IGNORE_LIST = ['__init__.py', 'santos-transparencia.py', 'settings.py']


def create_folders():
    if not os.path.isdir(CONTRATOS_PATH.absolute()):
        os.mkdir(CONTRATOS_PATH.absolute())

    if not os.path.isdir(LOCACOES_PATH.absolute()):
        os.mkdir(LOCACOES_PATH.absolute())

    if not os.path.isdir(CONVENIOS_PATH.absolute()):
        os.mkdir(CONVENIOS_PATH.absolute())

    if not os.path.isdir(DB_PATH.absolute()):
        os.mkdir(DB_PATH.absolute())


if __name__ == '__main__':

    files = os.listdir('.')
    modulos = ['Contratos', 'Convênios', 'Locações']
    files = [f for f in files if '.py' in f and f not in IGNORE_LIST]

    create_folders()

    for f, m in zip(sorted(files), sorted(modulos)):
        module_name = f.replace('.py', '')
        module = __import__(module_name)
        print('- Importando %s' % m)
        module.main()

