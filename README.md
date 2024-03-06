# Build image
```
docker build -t my-latex-image .
```

# docker run
## for linux & mac & Power Shell
```
docker run -idt --name my-latex -v "$(pwd):/app" -p 8080:8080  my-latex-image
```
## for cmd
```
docker run -idt --name my-latex -v %cd%:/app -p 8080:8080 my-latex-image
```
