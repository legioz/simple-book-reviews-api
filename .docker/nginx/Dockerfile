FROM nginx:alpine

ARG ENV=dev
RUN echo "Using ${ENV} environment!"
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.${ENV}.conf /etc/nginx/conf.d
COPY . /custom/config/
