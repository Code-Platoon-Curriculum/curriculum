FROM node:latest

WORKDIR /app

# Install dependencies
COPY package.json .
RUN npm install

# Copy all files and build the app
COPY . .

# Expose the port for the React app
EXPOSE 5173

# Start the React app
CMD ["npm", "run", "dev"]