FROM nginx:stable-alpine

COPY index.html /usr/share/nginx/html/index.html

COPY nginx.conf /etc/nginx/nginx.conf
COPY .htpasswd /etc/nginx/.htpasswd

EXPOSE 8198

CMD ["nginx", "-g", "daemon off;"]