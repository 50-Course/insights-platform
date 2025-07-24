.PHONY: backend web

dev:
	uvicorn backend.src.main:app --reload

backend:
	docker build -t ai-insights-backend -f backend/Dockerfile backend

web:
	docker build -t ai-insights-web -f web/Dockerfile web

run-backend:
	docker run -p 8000:8000 ai-insights-backend

run-web:
	docker run -p 80:80 ai-insights-web

clean:
	rm -rf web/build

