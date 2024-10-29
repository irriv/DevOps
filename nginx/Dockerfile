FROM nginx:stable-alpine

COPY index.html /usr/share/nginx/html/index.html

COPY nginx.conf /etc/nginx/nginx.conf
COPY .htpasswd /etc/nginx/.htpasswd

EXPOSE 8081

CMD ["nginx", "-g", "daemon off;"]