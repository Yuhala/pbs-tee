import requests

def scrape_devnet_metrics(rpc_url: str, metrics_port: int, metrics_path: str = '/metrics'):
    """
    Scrapes the Prometheus metrics endpoint of a local devnet and prints 
    the list of exposed metric names.

    :param rpc_url: The base URL of the devnet (e.g., "http://localhost").
    :param metrics_port: The port exposing the metrics (e.g., 6061).
    :param metrics_path: The specific path for metrics (usually "/metrics").
    """
    
    # Construct the full URL for the metrics endpoint
    url = f"{rpc_url.rstrip('/')}:{metrics_port}{metrics_path}"
    
    print(f"Attempting to scrape metrics from: {url}\n")
    
    try:
        # Make the GET request to the metrics port
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        
        # The content is a plain text response in Prometheus format
        metrics_data = response.text
        
        # --- Parsing the Metrics ---
        
        # Prometheus metrics are typically structured:
        # # HELP metric_name description...
        # # TYPE metric_name type
        # metric_name{labels...} value timestamp
        
        unique_metrics = set()
        
        for line in metrics_data.splitlines():
            # Lines starting with '#' are comments (HELP/TYPE) or empty
            if line.startswith('#'):
                # We specifically look for the line defining the metric type
                if line.startswith('# TYPE'):
                    # The metric name is the third token in this line: 
                    # # TYPE <metric_name> <type>
                    parts = line.split()
                    if len(parts) >= 3:
                        metric_name = parts[2]
                        unique_metrics.add(metric_name)
            # Non-comment lines are the metric values themselves
            elif line.strip():
                # The metric name is the part before the first brace '{' or space ' '
                if '{' in line:
                    metric_name = line.split('{', 1)[0].strip()
                else:
                    metric_name = line.split(' ', 1)[0].strip()
                    
                if metric_name:
                    unique_metrics.add(metric_name)


        print("--- Metrics Exposed ---")
        if unique_metrics:
            for metric in sorted(unique_metrics):
                print(f"- {metric}")
            print(f"\nTotal unique metrics found: {len(unique_metrics)}")
        else:
            print("No metrics found in the response.")
            
    except requests.exceptions.RequestException as e:
        print(f"Error scraping metrics: {e}")
        print("Ensure the devnet node is running and the port is accessible.")


# --- Configuration ---

# Replace with the IP/hostname of your devnet node
RPC_HOST = "http://127.0.0.1" 
EL_METRICS_PORT = 9090 # pyuhala: this works -> gets 294 metrics
OPNODE_METRICS_PORT = 7300 # pyuhala: 
OPGETH_METRICS_PORT = 6061 # doesn't work
METRICS_PORT = OPNODE_METRICS_PORT  # Your example port for op-get metrics
METRICS_ENDPOINT = "/metrics"

# Run the function
if __name__ == "__main__":
    scrape_devnet_metrics(RPC_HOST, METRICS_PORT, METRICS_ENDPOINT)