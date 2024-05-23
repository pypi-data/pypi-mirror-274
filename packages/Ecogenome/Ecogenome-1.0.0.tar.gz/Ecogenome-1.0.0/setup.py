from setuptools import setup

setup(
    name='Ecogenome',
    version='1.0.0',
    packages=[''],  # Ajoutez ici les noms de packages si vous avez plusieurs modules
    install_requires=[
        'PyQt5',  # Ajoutez ici les dépendances requises
    ],
    entry_points={
        'console_scripts': [
            'Ecogenome = test:main',  # Remplacez nom_de_votre_application et nom_de_votre_module_principal par vos valeurs
        ]
    },
)