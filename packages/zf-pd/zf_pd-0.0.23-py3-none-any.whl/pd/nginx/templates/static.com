server {
    server_name {{ domain }};

    root {{ static }};
    client_max_body_size 50M;

    location / {
        proxy_pass {{scheme}}://{{ host }}:{{ port }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias {{ static }};

        # Add CORS 'Access-Control-Allow-Origin' header for fonts
        location ~* \.(ico|png|css|ttf)$ {
            add_header Access-Control-Allow-Origin *;
        }
    }
}