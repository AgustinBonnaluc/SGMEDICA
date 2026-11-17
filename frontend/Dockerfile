FROM node:22-slim

WORKDIR /codigo

COPY package.json package-lock.json ./
RUN npm install

COPY . .

# --host permite entrar desde fuera del contenedor
CMD ["npm", "run", "dev", "--", "--host"]
