.PHONY: deps run

# regenerate requirements.txt with pipreqs
deps:
	pipreqs . --force --ignore ".venv,venv,env,build,dist,src/outputs"

# run a module by name, e.g.: make run module=module-1 args="--name OpenAI"
run:
	python -m src.main $(module) $(args)