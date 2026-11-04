# The edge suite with the kubectl its Kubernetes cases call.
FROM python:3.9.20-slim-bookworm
ADD https://dl.k8s.io/release/v1.28.15/bin/linux/amd64/kubectl /usr/local/bin/kubectl
RUN chmod 0755 /usr/local/bin/kubectl
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY . /work/e2e-edge-test-suite
WORKDIR /work/e2e-edge-test-suite
ENV PYTHONPATH=/work/e2e-edge-test-suite
