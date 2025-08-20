## Comparing Kata-TDX VM-containers to regular TDX VMs
The purpose of this is to understand the differences (if any) in performance between Kata-based TDX VMs to regular (manually created) TDX VMs. Since the components we deploy perform mostly network-based communication, our first benchmark focuses on this.

- We use `wrk`, an HTTP benchmarking tool. Setup and build `wrk` as follows.
```bash
# 1. install openssl 
sudo apt update
sudo apt install openssl net-tools libssl-dev unzip -y
# 2. Download and build wrk
git clone https://github.com/wg/wrk.git && cd wrk
make 
```
- Setup an HTTP server on the host to listen for connections
```bash
sudo apt install nginx -y
sudo systemctl start nginx
```
- If `nginx` port already in use, modify config in `/etc/nginx/sites-available/default` to use something different, e.g., `8080`
```bash
listen 8080 default_server;
listen [::]:8080 default_server;
```
- Test the config with `sudo nginx -t` and start with `sudo systemctl start nginx`. This should make `nginx` reachable from `http://127.0.0.1:8080`.
- Run a simple test with `wrk` as follows:
```bash
./wrk -t4 -c100 -d30s http://127.0.0.1:8080/
```
The above command runs wrk which uses 4 threads to generate connections independently towards the target URL. The total test duration is 30s.
The results generated are: requests per second, latency stats, total requests sent. 
- Below represents the results when running `wrk and nginx on the same host`
```bash
Running 30s test @ http://127.0.0.1:8080/
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   646.74us    0.95ms  27.51ms   92.63%
    Req/Sec    40.85k     5.43k   70.05k    68.92%
  4879138 requests in 30.01s, 49.63GB read
Requests/sec: 162588.64
Transfer/sec:      1.65GB
```

### Nginx in regular TDX VM and wrk on host
- My VM's IP is: `192.168.122.100` and is running nginx on port 8080. So from the host I launch wrk as follows.
```bash
./wrk -t4 -c100 -d30s http://192.168.122.100:8080/
```
- To verify that the VM is actually receiving `wrk` requests, check the Nginx access logs
```bash
sudo tail -f /var/log/nginx/access.log
```
The above should show many entries from `wrk` requests, for example.
```bash
192.168.122.1 - - [20/Aug/2025:10:11:55 +0000] "GET / HTTP/1.1" 200 615 "-" "-"
192.168.122.1 - - [20/Aug/2025:10:11:55 +0000] "GET / HTTP/1.1" 200 615 "-" "-"
...
```
My host machine has IP `192.168.122.1` so the TDX VM is indeed receiving the `wrk` requests.

 The results from the `wrk` run are as follows.
```bash
Running 30s test @ http://192.168.122.100:8080/
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     3.22ms    2.71ms  32.92ms   78.31%
    Req/Sec     8.78k     1.14k   14.80k    71.33%
  1049350 requests in 30.02s, 862.63MB read
Requests/sec:  34951.73
Transfer/sec:     28.73MB
```

### Nginx in Kata-TDX VM and wrk in normal Kata container
We build two pods: one for wrk and another for the nginx server; both will be in the Kubernetes network so can communicate directly.
Create both pods as follows
```bash
k apply -f kata-nginx-pod.yaml -f kata-wrk-pod.yaml
```
- Exec into the wrk pod and build and install wrk.
```bash
k exec -it kata-wrk -- /bin/bash
apt update
apt install openssl net-tools libssl-dev unzip wrk -y
```
Note: `k` is an alias for `k3s kubectl` on our system.
- Run the wrk bench
```bash
wrk -t4 -c100 -d30s http://nginx-service:80/
```
- Verify the Nginx pod is receiving the requests
```bash
k exec -it nginx-kata -- /bin/bash
tail -f /var/log/nginx/access.log
```
- The results obtained are
```bash
Running 30s test @ http://nginx-service:80/
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     2.20ms  780.03us  38.52ms   84.48%
    Req/Sec    11.40k     0.91k   13.73k    69.50%
  1361655 requests in 30.01s, 1.09GB read
Requests/sec:  45368.34
Transfer/sec:     37.30MB
```

### Nginx and wrk in TDX VM (without kubernetes)
```bash
Running 30s test @ http://127.0.0.1:8080/
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     2.45ms    3.85ms  55.95ms   89.17%
    Req/Sec    20.38k     6.26k   40.13k    65.00%
  365107 requests in 4.51s, 300.14MB read
Requests/sec:  80986.99
Transfer/sec:     66.58MB
```

### Nginx and wrk in TDX VM with kubernetes