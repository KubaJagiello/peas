# Base image for building the app
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json for dependency installation
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire project to the container
COPY . .

# Start the React development server
CMD ["npm", "start"]

# Expose the port React dev server runs on (3000 by default)
EXPOSE 3000

