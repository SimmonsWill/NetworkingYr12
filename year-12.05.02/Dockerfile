FROM alpine:3.19
RUN apk add --no-cache openssh-server
RUN adduser -D -s /bin/sh docker.05.02 && \
	echo "docker.05.02:docker.05.02" | chpasswd
RUN ssh-keygen -A
RUN printf 'Port 22\nPasswordAuthentication yes\nPermitRootLogin no\n' \
	> /etc/ssh/sshd_config
RUN echo "FLAG{y0u_f0und_th3_s3cr3t_f1l3}" \
	> /home/docker.05.02/secret.flag
RUN mkdir -p /run/sshd
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
