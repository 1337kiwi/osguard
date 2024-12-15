#!/bin/sh

# This should match the IMAGE_BASE variable in your Makefile
IMAGE_BASE="ctf2024-nl2sh"

# This is the port that xinetd will listen on/forward to spawned containers
# (i.e., this is the port that you will have Traefik configured to send ingress
# traffic to from the edge/firewall).
OUTER_PORT=41715

# Modify the rest with care; probably only if you need to adjust 
# the xinetd limits or the docker-run parameters (server_args).
#---------------------------------------------------------------

VERSION="$1"
INSTALL="$2"
if [ -z "$1" -o -z "$2" ]; then
	echo "usage: $0 VERSION_TAG INSTALL_PATH"
	exit 1
fi

cat >"$INSTALL" <<EOF
service ${IMAGE_BASE} 
{
	type = UNLISTED
	disable = no
	socket_type = stream
	protocol = tcp
	wait = no
	user = root
	instances = UNLIMITED
	port = ${OUTER_PORT}
	server = /usr/bin/docker
	server_args = run -i --init --rm --pids-limit=4 --cpus=0.5 --memory=100M --read-only --log-driver none --tmpfs /tmp:rw,noexec,nosuid,size=16M ${IMAGE_BASE}:${VERSION}
}
EOF

