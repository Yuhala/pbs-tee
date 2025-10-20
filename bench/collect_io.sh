#!/bin/bash


# Variables
NAMESPACE="test-2"
OUTPUT="pod_io_stats.csv"
DURATION=30   # total seconds
INTERVAL=1    # sampling interval
KUBECTL="sudo /usr/local/bin/k3s kubectl"   

# CSV header
echo "timestamp,pod,rx_bytes,tx_bytes,read_sectors,write_sectors" > $OUTPUT

# Get all pods in namespace
PODS=$($KUBECTL get pods -n $NAMESPACE --no-headers -o custom-columns=":metadata.name")

for POD in $PODS; do
    echo "Collecting stats for pod: $POD"

    for ((i=1; i<=DURATION; i++)); do
        TS=$(date +%s)

        # --- Network stats ---
        NET_LINE=$($KUBECTL exec -n $NAMESPACE $POD -- cat /proc/net/dev 2>/dev/null | grep -E "eth0|ens" | awk '{print $2","$10}')
        RX=$(echo $NET_LINE | cut -d',' -f1)
        TX=$(echo $NET_LINE | cut -d',' -f2)

        # --- Disk stats ---
        DISK_LINE=$($KUBECTL exec -n $NAMESPACE $POD -- cat /proc/diskstats 2>/dev/null | head -n 1 | awk '{print $6","$10}')
        READ=$(echo $DISK_LINE | cut -d',' -f1)
        WRITE=$(echo $DISK_LINE | cut -d',' -f2)

        # Append to CSV
        echo "$TS,$POD,$RX,$TX,$READ,$WRITE" >> $OUTPUT

        sleep $INTERVAL
    done
done

echo "✅ Results saved in $OUTPUT"
