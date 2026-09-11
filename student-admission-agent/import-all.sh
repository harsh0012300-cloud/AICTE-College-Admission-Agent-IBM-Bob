#!/usr/bin/env bash
# =============================================================================
# Student Admission Agent — Import Script
# Imports all tools and agents into watsonx Orchestrate using the ADK CLI.
# Usage: bash import-all.sh
# =============================================================================

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo "============================================================"
echo "  Student Admission Agent — watsonx Orchestrate Import"
echo "============================================================"

# -----------------------------------------------------------------------------
# Step 1: Import Python Tools
# -----------------------------------------------------------------------------
echo ""
echo "[1/3] Importing Python tools..."

for tool in admission_tools.py; do
  echo "  → Importing tool: ${tool}"
  orchestrate tools import -k python -f "${SCRIPT_DIR}/tools/${tool}"
done

echo "  ✓ Python tools imported."

# -----------------------------------------------------------------------------
# Step 2: Import OpenAPI Tool (Application Status API)
# -----------------------------------------------------------------------------
echo ""
echo "[2/3] Importing OpenAPI tool (Application Status API)..."

orchestrate tools import -k openapi -f "${SCRIPT_DIR}/tools/check_application_status_openapi.yaml"

echo "  ✓ OpenAPI tool imported."

# -----------------------------------------------------------------------------
# Step 3: Import Agent
# -----------------------------------------------------------------------------
echo ""
echo "[3/3] Importing agent..."

for agent in student_admission_agent.yaml; do
  echo "  → Importing agent: ${agent}"
  orchestrate agents import -f "${SCRIPT_DIR}/agents/${agent}"
done

echo "  ✓ Agent imported."

# -----------------------------------------------------------------------------
# Done
# -----------------------------------------------------------------------------
echo ""
echo "============================================================"
echo "  Import complete!"
echo ""
echo "  To start a chat session, run:"
echo "    orchestrate chat start"
echo ""
echo "  Then select 'student_admission_agent' from the list."
echo "============================================================"
