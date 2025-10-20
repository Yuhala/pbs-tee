Since you're running your devnet on a remote server, you'll need to install **Prometheus** and **Grafana** on that same server. Then, you can use **SSH port forwarding** to access Grafana's web interface on your local machine, where you can visualize the data.

### 1\. Install Prometheus on the Server

The most common way to install Prometheus on an Ubuntu server is by downloading the pre-compiled binaries and setting it up as a systemd service.

1.  **Create a Prometheus user and directories**: For security, create a dedicated user for Prometheus and the necessary directories for its configuration and data.

    ```bash
    sudo useradd --no-create-home --shell /bin/false prometheus
    sudo mkdir /etc/prometheus
    sudo mkdir /var/lib/prometheus
    ```

2.  **Download and extract Prometheus**: Find the download link for the latest Linux version from the official Prometheus website.

    ```bash
    wget https://github.com/prometheus/prometheus/releases/download/<VERSION>/prometheus-<VERSION>.linux-amd64.tar.gz
    tar xvf prometheus-<VERSION>.linux-amd64.tar.gz
    cd prometheus-<VERSION>.linux-amd64
    ```

3.  **Move the binaries and configure permissions**: Move the `prometheus` and `promtool` binaries to a standard location and set the correct ownership.

    ```bash
    sudo mv prometheus promtool /usr/local/bin/
    sudo chown prometheus:prometheus /usr/local/bin/prometheus
    sudo chown prometheus:prometheus /usr/local/bin/promtool
    sudo mv consoles/ console_libraries/ /etc/prometheus/
    sudo mv prometheus.yml /etc/prometheus/prometheus.yml
    sudo chown -R prometheus:prometheus /etc/prometheus/
    sudo chown -R prometheus:prometheus /var/lib/prometheus/
    ```

4.  **Edit the `prometheus.yml` configuration file**: Use `nano` or a similar text editor to configure Prometheus to scrape the metrics from your devnet. Add a scrape job for each component.

    ```yaml
    # /etc/prometheus/prometheus.yml
    global:
      scrape_interval: 15s

    scrape_configs:
      - job_name: 'el-geth'
        static_configs:
          - targets: ['localhost:9090']

      - job_name: 'op-geth'
        static_configs:
          - targets: ['localhost:6061']

      - job_name: 'op-node'
        static_configs:
          - targets: ['localhost:7300']
    ```
    - The above ports are for the default config. Based on Claudiu's new configs, maybe we should use [this file](./prometheus.yml).
   

5.  **Create a systemd service file**: This allows Prometheus to run as a background service.

    ```bash
    sudo nano /etc/systemd/system/prometheus.service
    ```

    Add the following content, save, and exit:

    ```ini
    [Unit]
    Description=Prometheus
    Wants=network-online.target
    After=network-online.target

    [Service]
    User=prometheus
    Group=prometheus
    Type=simple
    ExecStart=/usr/local/bin/prometheus \
      --config.file=/etc/prometheus/prometheus.yml \
      --storage.tsdb.path=/var/lib/prometheus/

    [Install]
    WantedBy=multi-user.target
    ```

6.  **Start and enable the service**:

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start prometheus
    sudo systemctl enable prometheus
    sudo systemctl status prometheus
    ```

-----

### 2\. Install Grafana on the Server

1.  **Add the Grafana APT repository**:

    ```bash
    sudo apt-get install -y apt-transport-https software-properties-common wget
    wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
    echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
    sudo apt-get update
    ```

2.  **Install Grafana**:

    ```bash
    sudo apt-get install grafana
    ```

3.  **Start and enable the Grafana service**:

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start grafana-server
    sudo systemctl enable grafana-server
    ```

By default, Grafana runs on port **3000**.

-----

### 3\. Visualize Metrics on Your Host PC

To access the Grafana dashboard from your local machine, you'll use **SSH port forwarding** to tunnel the Grafana port.

1.  **Open a local terminal** and run the SSH command:

    ```bash
    ssh -L 3000:localhost:3000 <YOUR_USERNAME>@<REMOTE_SERVER_ADDRESS>
    ```

2.  **Access Grafana**: Now, open your web browser on your local machine and navigate to `http://localhost:3000`. You'll be able to access the Grafana login page. The default credentials are `admin` for both the username and password. You will be prompted to change the password upon first login.

3.  **Connect Prometheus as a data source**:

      * In the Grafana UI, click the **Connections** icon on the left sidebar, then **Data sources**.
      * Click **Add data source** and select **Prometheus**.
      * In the URL field, enter `http://localhost:9090` (since Prometheus is running on the same server, `localhost` is correct for Grafana).
      * Click **Save & test**. Grafana will now be connected to your Prometheus instance.

4.  **Build a Dashboard**: You can now create panels and use PromQL queries to visualize your devnet's metrics.

[A video about setting up a monitoring stack with Prometheus, Grafana, and Tailscale is provided below.](https://www.youtube.com/watch?v=ChXN7pDTo5k) This video is relevant as it shows how to use Prometheus and Grafana for remote monitoring.
http://googleusercontent.com/youtube_content/3



### Debugging metrics ports
- List all pod IPs in a namespace (e.g., `test-2`)
```bash
k get pods -n test-2 -o custom-columns=NAME:.metadata.name,IP:.status.podIP
```
- Check each pod if it is listening on port
```bash
k exec -n test-2 op-node-7b8f5bdb4b-kxw9c -- netstat -tuln | grep 7300
```
- Check logs for metrics server start
```bash
k logs -n test-2 op-node-7b8f5bdb4b-kxw9c | grep -i metrics
```
- Find metrics port
```bash
k logs -n test-2 op-node-7b8f5bdb4b-kxw9c | grep -i "metrics\|server\|listen\|port"
```
- If the `curl` commands work, then they should be shown in Prometheus too.
```bash
curl -v http://10.42.0.52:7300/metrics
curl -v http://10.42.0.51:6061/metrics
curl -v http://10.42.0.49:9090/metrics
curl -v http://10.42.0.87:8080/metrics
```

