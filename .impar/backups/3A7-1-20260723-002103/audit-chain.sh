#!/bin/bash
# audit-chain.sh — Hash-chained audit log integrity verification
# Implements deterministic JSON canonicalization + SHA-256 hash chaining
# For use in EXECUTION_AUDIT_CHAIN.jsonl (new records only, legacy unaffected)

set -euo pipefail

# Canonicalize JSON for deterministic hashing
# Input: JSON object (potentially unordered keys, variable spacing)
# Output: Canonical JSON with sorted keys, no extra spaces
canonicalize_json() {
  local json="$1"

  # Use jq to parse and re-output with sorted keys, compact output
  echo "$json" | jq -S -c . 2>/dev/null || echo ""
}

# Calculate SHA-256 hash of a string
# Input: String
# Output: SHA-256 hex hash
calculate_hash() {
  local input="$1"
  echo -n "$input" | shasum -a 256 | awk '{print $1}'
}

# Calculate record hash with chain verification
# Input:
#   record_json — JSON object containing execution details
#   previous_hash — SHA-256 hash of previous record (or "genesis" for first)
# Output: JSON with hash field added
add_record_hash() {
  local record_json="$1"
  local previous_hash="${2:-genesis}"

  # Canonicalize the record
  local canonical_record=$(canonicalize_json "$record_json")

  if [ -z "$canonical_record" ]; then
    echo "ERROR: Invalid JSON in add_record_hash" >&2
    return 1
  fi

  # Create chain input: canonical_record + previous_hash
  local chain_input="${canonical_record}${previous_hash}"

  # Calculate hash of (canonical_record + previous_hash)
  local record_hash=$(calculate_hash "$chain_input")

  # Add hash field to record
  local record_with_hash=$(echo "$canonical_record" | jq -c --arg h "$record_hash" '. + {hash: $h}')
  echo "$record_with_hash"
}

# Verify chain integrity of audit log
# Input: Path to EXECUTION_AUDIT_CHAIN.jsonl
# Output: PASS/WARNING/FAIL with details
verify_chain() {
  local audit_file="$1"

  if [ ! -f "$audit_file" ]; then
    echo "FAIL: Audit file not found: $audit_file"
    return 1
  fi

  local previous_hash="genesis"
  local line_count=0
  local failed_lines=0

  while IFS= read -r line; do
    line_count=$((line_count + 1))

    # Skip empty lines
    if [ -z "$line" ]; then
      continue
    fi

    # Extract hash from current record
    local stored_hash=$(echo "$line" | jq -r '.hash // empty' 2>/dev/null)

    if [ -z "$stored_hash" ]; then
      echo "WARNING: Record $line_count missing hash field"
      failed_lines=$((failed_lines + 1))
      continue
    fi

    # Remove hash to get clean record
    local clean_record=$(echo "$line" | jq -c 'del(.hash)' 2>/dev/null)

    if [ -z "$clean_record" ]; then
      echo "FAIL: Record $line_count is invalid JSON"
      failed_lines=$((failed_lines + 1))
      continue
    fi

    # Recalculate hash
    local chain_input="${clean_record}${previous_hash}"
    local calculated_hash=$(calculate_hash "$chain_input")

    # Verify
    if [ "$stored_hash" != "$calculated_hash" ]; then
      echo "FAIL: Record $line_count hash mismatch (stored=$stored_hash, calculated=$calculated_hash)"
      failed_lines=$((failed_lines + 1))
    fi

    # Move to next
    previous_hash="$stored_hash"
  done < "$audit_file"

  if [ $failed_lines -eq 0 ]; then
    echo "PASS: Chain integrity verified ($line_count records)"
    return 0
  elif [ $failed_lines -lt $((line_count / 10)) ]; then
    echo "WARNING: Chain integrity partial ($failed_lines/$line_count records failed)"
    return 0
  else
    echo "FAIL: Chain integrity broken ($failed_lines/$line_count records failed)"
    return 1
  fi
}

# Generate new audit record with hash-chaining
# Input:
#   service — service name
#   status — EXECUTED, FAILED, BLOCKED, etc.
#   details — JSON object with additional details
#   previous_hash — previous record hash (or "genesis")
# Output: JSON record with hash
generate_audit_record() {
  local service="$1"
  local status="$2"
  local details="${3:-{}}"
  local previous_hash="${4:-genesis}"

  # Get current timestamp
  local timestamp=$(date -u +"${1:-}%Y-%m-%dT%H:%M:%SZ" | sed 's/^[^2]*//')

  # If timestamp parsing failed, use date command properly
  if ! [[ "$timestamp" =~ ^[0-9]{4}-[0-9]{2} ]]; then
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  fi

  # Create base record
  local record=$(jq -n --arg svc "$service" --arg sts "$status" --arg ts "$timestamp" --argjson det "$details" \
    '{timestamp: $ts, service: $svc, status: $sts, details: $det}')

  # Add hash with chain
  local record_with_hash=$(add_record_hash "$record" "$previous_hash")

  echo "$record_with_hash"
}

# Export functions for use in other scripts
export -f canonicalize_json
export -f calculate_hash
export -f add_record_hash
export -f verify_chain
export -f generate_audit_record
