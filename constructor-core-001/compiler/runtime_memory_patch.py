def apply_memory_guard(result, max_depth=5):

    def trim(node, depth=0):
        if node is None:
            return None

        if depth > max_depth:
            return None

        if isinstance(node, dict):
            if "prev_state" in node:
                node["prev_state"] = trim(node["prev_state"], depth + 1)

        return node

    return trim(result)
