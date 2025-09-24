#!/bin/bash

TARGET_POD="<target_pod_name>"   # Select target pod among benign pods
ATTACKER_DIR="<attack_pods_directory>"   # Select the attack pod directory corresponding to the attack strategy to be evaluated
MAX_ATTEMPTS=20   # Maximum number of attempts per test
TOTAL_RUNS=120    # Total number of tests
TOTAL_ATTEMPTS=0  # Total number of attempts
SUCCESS_COUNT=0   # Number of successful collocations

RESULT_FILE="colocation_results.txt"
ATTACKER_BASENAME="attack-pod"  

# result file initialize
echo "=== Colocation Test Results ===" > $RESULT_FILE
echo "Target Pod: $TARGET_POD" >> $RESULT_FILE
echo "Total Runs: $TOTAL_RUNS" >> $RESULT_FILE
echo "Max Attempts per Run: $MAX_ATTEMPTS" >> $RESULT_FILE
echo "================================" >> $RESULT_FILE
echo "" >> $RESULT_FILE

# Find the node where target pod is running
TARGET_NODE=$(kubectl get pod "$TARGET_POD" -o jsonpath='{.spec.nodeName}')

if [ -z "$TARGET_NODE" ]; then
    echo "Error: Failed to determine node of target pod $TARGET_POD."
    exit 1
fi

echo "Target Pod ($TARGET_POD) is running on Node: $TARGET_NODE"
echo "Starting colocation test for $TOTAL_RUNS iterations..."

for ((run=1; run<=TOTAL_RUNS; run++)); do
    echo "***********************************************"
    echo "Test Run #$run"

    for ((i=1; i<=MAX_ATTEMPTS; i++)); do
        ATTACKER_YAML="$ATTACKER_DIR/$ATTACKER_BASENAME-$i.yaml"

        if [ ! -f "$ATTACKER_YAML" ]; then
            echo "Error: $ATTACKER_YAML not found. Skipping..."
            continue
        fi

        kubectl apply -f "$ATTACKER_YAML" &> /dev/null
        sleep 5  

        ATTACKER_NODE=$(kubectl get pod "$ATTACKER_BASENAME-$i" -o jsonpath='{.spec.nodeName}')

        if [ "$ATTACKER_NODE" == "$TARGET_NODE" ]; then
            echo "Colocation achieved after $i attempts."
            TOTAL_ATTEMPTS=$((TOTAL_ATTEMPTS + i))
            SUCCESS_COUNT=$((SUCCESS_COUNT + 1))

            # Total CPU/MEM usage of all attack pods used in the attack
            TOTAL_CPU=0
            TOTAL_MEM=0

            for ((k=1; k<=i; k++)); do
                USAGE=$(kubectl top pod "$ATTACKER_BASENAME-$k" --no-headers 2>/dev/null)
                CPU=$(echo $USAGE | awk '{print $2}' | sed 's/m//')
                MEM=$(echo $USAGE | awk '{print $3}' | sed 's/Mi//')

                CPU=${CPU:-0}
                MEM=${MEM:-0}

                TOTAL_CPU=$((TOTAL_CPU + CPU))
                TOTAL_MEM=$((TOTAL_MEM + MEM))
            done

            # Save evaluation results to a file
            {
                echo "Run #$run"
                echo "  Attempts: $i"
                echo "  Total CPU Usage (all attack pods): ${TOTAL_CPU}m"
                echo "  Total Memory Usage (all attack pods): ${TOTAL_MEM}Mi"
                echo "  Node (colocated): $ATTACKER_NODE"
                echo "--------------------------------"
            } >> $RESULT_FILE

            break
        fi

        sleep 2
    done

    # Delete attack pod for next evaluation
    for ((j=1; j<=i; j++)); do
        kubectl delete pod "$ATTACKER_BASENAME-$j" --ignore-not-found=true --grace-period=0 --force &> /dev/null
    done

    sleep 3
done

if [ "$SUCCESS_COUNT" -gt 0 ]; then
    AVG_ATTEMPTS=$(echo "scale=2; $TOTAL_ATTEMPTS / $SUCCESS_COUNT" | bc)
    echo "***********************************************"
    echo "Average attempts to achieve colocation: $AVG_ATTEMPTS"
    echo "" >> $RESULT_FILE
    echo "=== Summary ===" >> $RESULT_FILE
    echo "Total Runs: $TOTAL_RUNS" >> $RESULT_FILE
    echo "Success Count: $SUCCESS_COUNT" >> $RESULT_FILE
    echo "Average Attempts: $AVG_ATTEMPTS" >> $RESULT_FILE
else
    echo "No successful colocation achieved."
    echo "No successful colocation achieved." >> $RESULT_FILE
fi
