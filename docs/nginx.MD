```
server {
    listen       80;
    listen       [::]:80;
    server_name  localhost;
    location / { 
        root    /home/wifi/autoweb/dist;
        index  index.html index.htm;
    }   
    location /api {
        proxy_pass 127.0.0.1:8005/api;
    }   
}
```
