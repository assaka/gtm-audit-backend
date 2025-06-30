# services/gtm_parser.py

def parse_gtm_file(data: dict) -> dict:
    """
    Takes the raw GTM containerVersion dict (parsed from JSON) and returns
    a structured summary including counts and key details of tags, triggers, and variables.
    """

    # Top-level container info
    container = data.get("containerVersion", {})
    info = container.get("container", {})
    public_id = info.get("publicId", "unknown")
    name = info.get("name", "unnamed container")

    # Collections
    tags = container.get("tag", [])
    triggers = container.get("trigger", [])
    variables = container.get("variable", [])

    # Simplify each tag
    simplified_tags = []
    for t in tags:
        simplified_tags.append({
            "name": t.get("name"),
            "type": t.get("type"),
            "firingTriggerIds": t.get("triggerId", []),
            "parameterCount": len(t.get("parameter", []))
        })

    # Simplify each trigger
    simplified_triggers = []
    for tr in triggers:
        filters = tr.get("filter", [])
        filter_list = []
        for f in filters:
            params = f.get("parameter", [])
            vals = [p.get("value") for p in params if p.get("value") is not None]
            filter_list.append({
                "type": f.get("type"),
                "values": vals
            })

        simplified_triggers.append({
            "name": tr.get("name"),
            "type": tr.get("type"),
            "filterCount": len(filters),
            "filters": filter_list
        })

    # Simplify each variable
    simplified_vars = []
    for v in variables:
        simplified_vars.append({
            "name": v.get("name"),
            "type": v.get("type"),
            "parameterCount": len(v.get("parameter", []))
        })

    return {
        "containerId": public_id,
        "containerName": name,
        "tagCount": len(tags),
        "triggerCount": len(triggers),
        "variableCount": len(variables),
        "tags": simplified_tags,
        "triggers": simplified_triggers,
        "variables": simplified_vars
    }
