# Use a lightweight Node image suitable for front-end tooling
FROM node:18-alpine

# Set working directory inside the container
WORKDIR /usr/src/app

# Copy package manifest to leverage cached dependency installation
COPY webPage/package*.json ./webPage/

# Install production and development dependencies required by gulp workflow
RUN cd webPage \
    && npm install --no-audit --no-fund

# Copy project sources required during runtime
COPY webPage ./webPage
COPY plant ./plant

# Switch into the webPage directory where gulp expects to run
WORKDIR /usr/src/app/webPage

# BrowserSync exposes both the UI (3001) and the preview server (3000)
EXPOSE 3000 3001

# Default command installs missing dependencies (first-run) before starting gulp dev server
CMD ["sh", "-c", "npm install --no-audit --no-fund && npm run dev"]
