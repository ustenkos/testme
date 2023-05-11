#!/bin/bash

### MANDATORY ### define the cnvrg cluster domain:
CLUSTER_DOMAIN=$1

### OPTIONAL  ### define the PYPI server username:
PYPI_USERNAME="itayosadminos"

### no intervention/modifications needed going forward ###

# add helm repo:
helm repo add owkin https://owkin.github.io/charts

# create credentials secret
PYPI_PASSWORD=$(echo -n $PYPI_USERNAME | md5sum | cut -c 1-32)
FULL=$PYPI_USERNAME:$PYPI_PASSWORD

mkdir pypi_tmp && cd pypi_tmp
echo $FULL > .htpasswd

kubectl create ns pypi
kubectl -n pypi create secret generic pypi-creds --from-file=.htpasswd

# install pypi server    
helm install -n pypi pypiserver owkin/pypiserver \
--set persistence.enabled=true \
--set persistence.size="3Gi" \
--set pypiserver.extraArgs={"--overwrite"} \
--set auth.existingSecret=pypi-creds \
--set resources.requests.cpu="100m" \
--set resources.requests.memory="100Mi" \
--debug

# expose pypi server using istio VS
kubectl -n cnvrg apply -f - <<EOF
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: pypi
  namespace: cnvrg
spec:
  gateways:
    - istio-gw-cnvrg
  hosts:
    - pypi.$CLUSTER_DOMAIN
  http:
    - retries:
        attempts: 5
        perTryTimeout: 172800s
      route:
        - destination:
            host: pypiserver-pypiserver.pypi.svc.cluster.local
      timeout: 864000s
EOF

# to upload python packages to server, install twine utility:
pip install twine

# download packages required as dependencies for cnvrg jobs:
pip download --dest . tensorboard jupyterlab jupyterlab-git gunicorn \
dash dash-daq voila pygments flask pika plumber faust-streaming dataclasses

# upload the packages to pypi server:
twine upload --repository-url \
http://pypi.$CLUSTER_DOMAIN \
--username $PYPI_USERNAME --password $PYPI_PASSWORD \
*.whl

cd .. && rm -rf pypi_tmp/
echo "PYPI server is ready!"

# pypi index url will be:
PYPI_INDEX_URL="http://pypi.$CLUSTER_DOMAIN/simple"
echo "index URL: $PYPI_INDEX_URL"

# use this link to access in browser:
PYPI_INDEX_UI="http://pypi.$CLUSTER_DOMAIN/packages"
echo "WHL folder for browsing: $PYPI_INDEX_UI"

echo "username: $PYPI_USERNAME"
echo "password: $PYPI_PASSWORD"

# after server setup completed, verify these steps:
# 1- define custom pypi server in org settings
# 2- verify "install deps" is toggled in org settings
# 3- run any kind of cnvrg job twice: once using v5 image, the second time using nvcr.io/nvidia/pytorch:23.01-py3
# 4- verify all deps installation were succesful
# 5- check in logs that all files were fetched from the custom pypi server only, and not from main pypi.org
