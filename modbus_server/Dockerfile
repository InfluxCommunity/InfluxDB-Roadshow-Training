FROM golang:latest

# Set the working directory inside the container
WORKDIR /app

COPY src/ .

# Download dependencies and build the Go application
RUN go mod download
RUN go build -o modbus_server

# Expose the port the application will run on (modify as needed)
EXPOSE 1502

CMD ["/app/modbus_server", "/app/config.json"]