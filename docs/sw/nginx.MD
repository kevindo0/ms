### 1.

### 2. 使用
#### 1. 端口转发
```
server {
        listen 80;
        location / {
            proxy_pass http://127.0.0.1:8081/;
        }
        location /api {
            proxy_pass http://127.0.0.1:5000/api;
        }
}
```
