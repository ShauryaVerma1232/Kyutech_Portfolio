
  # =============================================================================
  # Day 02 — CTM Attack Path Scoring (Pure Python, Self-Contained)
  # =============================================================================
  # This script rebuilds the _score_path logic from scratch using ONLY:
  #   dicts, lists, sets, tuples, comprehensions.
  # No imports. No NetworkX. No dataclasses.

  # ── 1. Constants ─────────────────────────────────────────────────────────────

NT_INTERNET  = "INTERNET"
NT_EC2       = "EC2"
NT_IAM_ROLE  = "IAM_ROLE"
NT_IAM_USER  = "IAM_USER"
NT_S3        = "S3_BUCKET"
NT_RDS       = "RDS"

ET_EXPOSES     = "exposes"
ET_ASSUMES     = "assumes_role"
ET_CAN_ACCESS  = "can_access"

IMPACT_WEIGHTS = {
    NT_S3:        0.80,
    NT_RDS:       0.90,
    NT_IAM_ROLE:  0.70,
    NT_EC2:       0.50,
    NT_IAM_USER:  0.60,
    NT_INTERNET:  0.00,
  }


  # ── 2. Toy Graph (built by hand) ─────────────────────────────────────────────

  # Nodes: {node_id: {attributes}}
nodes = {
    "INTERNET": {
        "node_type": NT_INTERNET,
        "label": "Internet",
        "public": True,
        "metadata": {},
      },
    "ec2-web": {
        "node_type": NT_EC2,
        "label": "EC2: web-server",
        "public": True,
        "metadata": {
            "instance_type": "t2.micro",
            "imdsv1_enabled": True,   # <-- Known exploit boost
            "public_ip": "3.84.12.34",
          },
      },
    "role-admin": {
        "node_type": NT_IAM_ROLE,
        "label": "Role: admin-role",
        "public": False,
        "metadata": {
            "role_name": "admin-role",
            "is_admin": True,          # <-- Impact boost
            "scope": "admin",
          },
      },
    "s3-secrets": {
        "node_type": NT_S3,
        "label": "S3: secrets-bucket",
        "public": False,
        "metadata": {
            "bucket_name": "secrets-bucket",
            "is_public": False,
          },
      },
  }

  # Adjacency: {source: {target: {edge_attributes}}}
adj = {
    "INTERNET": {
        "ec2-web": {"edge_type": ET_EXPOSES, "weight": 1.0},
      },
    "ec2-web": {
        "role-admin": {"edge_type": ET_ASSUMES, "weight": 0.8},
      },
    "role-admin": {
        "s3-secrets": {"edge_type": ET_CAN_ACCESS, "weight": 0.75},
      },
    "s3-secrets": {},   # Terminal node
  }


  # ── 3. Helpers ───────────────────────────────────────────────────────────────

def classify_severity(score):
    if score >= 8.0:
          return "critical"
    if score >= 6.0:
          return "high"
    if score >= 3.5:
          return "medium"
    return "low"


def path_string(node_ids):
    labels = [nodes[n]["label"] for n in node_ids]
    return " → ".join(labels)


  # ── 4. Core scoring logic (rewritten from _score_path) ───────────────────────

def score_path(node_ids, source_type):
      """
      Compute the multi-factor risk score for a single attack path.
      Returns a plain dict (no dataclass, no NetworkX).
      """

      # ── Build edge list from consecutive node pairs ──────────────────────────
      edges = []
      for i in range(len(node_ids) - 1):
          src, tgt = node_ids[i], node_ids[i + 1]
          edge_data = adj[src][tgt]          # dict lookup instead of G.edges[src,tgt]

          edges.append({
              "source": src,
              "target": tgt,
              "edge_type": edge_data.get("edge_type", "unknown"),
              "weight": edge_data.get("weight", 0.5),
          })

      # ── Reachability: fraction of edges with weight >= 0.7 ─────────────────
      if edges:
          easy = sum(1 for e in edges if e["weight"] >= 0.7)
          reachability = easy / len(edges)
      else:
          reachability = 0.0

      # ── Impact: value of the terminal node ─────────────────────────────────
      terminal = node_ids[-1]
      terminal_type = nodes[terminal]["node_type"]
      impact = IMPACT_WEIGHTS.get(terminal_type, 0.5)

      # Admin role boost
      if terminal_type == NT_IAM_ROLE:
          meta = nodes[terminal].get("metadata", {})
          if meta.get("is_admin"):
              impact = min(impact + 0.25, 1.0)

      # ── Exploitability: penalize hop count, then apply boosts ──────────────
      hop_count = len(node_ids) - 1
      exploitability = max(0.0, 1.0 - (hop_count - 1) * 0.15)

      # IMDSv1 boost: if ANY node in path has imdsv1_enabled
      for nid in node_ids:
          meta = nodes[nid].get("metadata", {})
          if meta.get("imdsv1_enabled"):
              exploitability = min(exploitability + 0.2, 1.0)
              break

      # Credential-based origin boost
      if source_type == "credential":
          exploitability = min(exploitability + 0.15, 1.0)

      # ── Exposure: how exposed is the entry point? ──────────────────────────
      if source_type == "network":
          if len(node_ids) > 1:
              second_node = nodes[node_ids[1]]
              first_edge = edges[0] if edges else {}
              if first_edge.get("edge_type") == ET_EXPOSES and second_node.get("public"):
                  exposure = 1.0
              elif second_node.get("public"):
                  exposure = 0.7
              else:
                  exposure = 0.3
          else:
              exposure = 0.0
      else:
          exposure = 0.8

      # ── Composite score ────────────────────────────────────────────────────
      risk_score = (
          reachability   * 0.30 +
          impact         * 0.35 +
          exploitability * 0.25 +
          exposure       * 0.10
      ) * 10.0

      return {
          "path_nodes": node_ids,
          "path_edges": edges,
          "path_string": path_string(node_ids),
          "reachability_score": round(reachability, 4),
          "impact_score": round(impact, 4),
          "exploitability_score": round(exploitability, 4),
          "exposure_score": round(exposure, 4),
          "risk_score": round(risk_score, 2),
          "severity": classify_severity(risk_score),
      }


  # ── 5. Run it ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
      # Example 1: Network-based attack (INTERNET → EC2 → Role)
      path_1 = ["INTERNET", "ec2-web", "role-admin"]
      result_1 = score_path(path_1, source_type="network")

      print("=" * 60)
      print("Path 1: " + result_1["path_string"])
      print("=" * 60)
      print(f"Reachability:   {result_1['reachability_score']}  (2 easy edges / 2 total)")
      print(f"Impact:         {result_1['impact_score']}  (IAM role + admin boost)")
      print(f"Exploitability: {result_1['exploitability_score']}  (2 hops + IMDSv1 boost)")
      print(f"Exposure:       {result_1['exposure_score']}  (network + exposes edge + public)")
      print(f"Risk Score:     {result_1['risk_score']}  ({result_1['severity'].upper()})")
      print()

      # Example 2: Credential-based attack (IAM User → Role → S3)
      # Add a user node for this second demo
      nodes["user-bilbo"] = {
          "node_type": NT_IAM_USER,
          "label": "User: bilbo",
          "public": False,
          "metadata": {"active_key_count": 1, "has_console": True},
      }
      adj["user-bilbo"] = {"role-admin": {"edge_type": ET_ASSUMES, "weight": 0.9}}

      path_2 = ["user-bilbo", "role-admin", "s3-secrets"]
      result_2 = score_path(path_2, source_type="credential")

      print("=" * 60)
      print("Path 2: " + result_2["path_string"])
      print("=" * 60)
      print(f"Reachability:   {result_2['reachability_score']}  (2 easy edges / 2 total)")
      print(f"Impact:         {result_2['impact_score']}  (S3 bucket)")
      print(f"Exploitability: {result_2['exploitability_score']}  (2 hops + credential boost)")
      print(f"Exposure:       {result_2['exposure_score']}  (credential origin)")
      print(f"Risk Score:     {result_2['risk_score']}  ({result_2['severity'].upper()})")
