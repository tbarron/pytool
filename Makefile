clean:
	PYENV_VERSION=2.7 xclean
	rm -rf {pytool,test}/__pycache__
