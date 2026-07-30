UV = uv


fmt:
	$(UV) run ruff check --select I --fix .
	$(UV) run ruff format . --no-cache
	@echo '[OK] Formatters went through successfully'

lint:
	$(UV) run ruff check solution --no-cache
	@echo '[OK] Linters checks passed successfully'

