clean:
	PYENV_VERSION=2.7 xclean -r
	rm -rf {pytool,test}/__pycache__
