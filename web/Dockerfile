# FROM cirrusci/flutter:latest
FROM ghcr.io/cirruslabs/flutter:3.32.8 AS build

WORKDIR /app

COPY . .

RUN flutter pub get
RUN flutter build web

FROM nginx:alpine
COPY --from=0 /app/build/web /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

