def register():

    return {
        "tests": [
            {
                "cmd": ["nmap", "-F", "127.0.0.1"],
                "desc": "Local scan"
            }
        ]
    }
