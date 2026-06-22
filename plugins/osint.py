def register():

    return {
        "tests": [
            {
                "cmd": ["curl", "-I", "https://google.com"],
                "desc": "HTTP headers fetch"
            },
            {
                "cmd": ["whoami"],
                "desc": "User context"
            }
        ]
    }
