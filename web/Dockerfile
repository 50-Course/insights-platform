FROM cirrusci/flutter:latest

WORKDIR /app

COPY web/ .

RUN flutter pub get
RUN flutter build web

FROM nginx:alpine
COPY --from=0 /app/build/web /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

