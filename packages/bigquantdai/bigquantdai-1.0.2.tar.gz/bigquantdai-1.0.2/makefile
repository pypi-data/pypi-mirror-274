include public/build/build.mk
SHELL := /bin/bash

sdk:
	python3 setup.py sdist bdist_wheel

sdk-nuitka:
	python3 setup.py bdist_nuitka

clean:
	rm -rf build dist bigquantdai.egg-info

# __token__
# pypi-AgEIcHlwaS5vcmcCJGM0Yjk1ZTkwLWVkYzUtNDI3ZC05NTYzLWZiZjU5NDMyNzJlOQACKlszLCI4MWIzN2IzZS0yMGI4LTQ3NzQtOWZiZS00MTAyMGJmMGUzMmIiXQAABiA7pUzODXezXMA38033EJk7a43SvLS6RGEk9j1edgMGAg
upload:
	python3 -m twine upload dist/*
