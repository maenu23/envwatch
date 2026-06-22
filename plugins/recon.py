def register():

    return {
        "tests": [
            {
                "cmd": ["ping", "-c", "1", "8.8.8.8"],
                "desc": "ICMP connectivity"
            },
            {
                "cmd": ["nslookup", "google.com"],
                "desc": "DNS resolution"
            }
        ]
    }
