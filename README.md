```
docker build -t my-image .
docker run -idt --name my-latex -v "$(pwd):/app" -p 8080:8080  my-image
```
