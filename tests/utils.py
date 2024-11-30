mock_filesystem = {
    "name": "interpreter",
    "size": 4096,
    "time_modified": 1699957865,
    "permissions": "-rw-r--r--",
    "contents": [
        {
            "name": ".gitignore",
            "size": 8911,
            "time_modified": 1699941437,
            "permissions": "-rw-r--r--"
        },
        {
            "name": "LICENSE",
            "size": 1071,
            "time_modified": 1699941437,
            "permissions": "-rw-r--r--"
        },
        {
            "name": "README.md",
            "size": 83,
            "time_modified": 1699941437,
            "permissions": "-rw-r--r--"
        },
        {
            "name": "ast",
            "size": 4096,
            "time_modified": 1699957739,
            "permissions": "drwxr-xr-x",
            "contents": [
                {
                    "name": "go.mod",
                    "size": 225,
                    "time_modified": 1699957780,
                    "permissions": "-rw-r--r--"
                },
                {
                    "name": "ast.go",
                    "size": 837,
                    "time_modified": 1699957719,
                    "permissions": "drwxr-xr-x"
                }
            ]
        },
        {
            "name": "go.mod",
            "size": 60,
            "time_modified": 1699950073,
            "permissions": "-rw-r--r--"
        },
        {
            "name": "lexer",
            "size": 4096,
            "time_modified": 1699955487,
            "permissions": "drwxr-xr-x",
            "contents": [
                {
                    "name": "lexer_test.go",
                    "size": 1729,
                    "time_modified": 1699955126,
                    "permissions": "drwxr-xr-x"
                },
                {
                    "name": "go.mod",
                    "size": 227,
                    "time_modified": 1699944819,
                    "permissions": "-rw-r--r--"
                },
                {
                    "name": "lexer.go",
                    "size": 2886,
                    "time_modified": 1699955487,
                    "permissions": "drwxr-xr-x"
                }
            ]
        },
        {
            "name": "main.go",
            "size": 74,
            "time_modified": 1699950453,
            "permissions": "-rw-r--r--"
        },
        {
            "name": "parser",
            "size": 4096,
            "time_modified": 1700205662,
            "permissions": "drwxr-xr-x",
            "contents": [
                {
                    "name": "parser_test.go",
                    "size": 1342,
                    "time_modified": 1700205662,
                    "permissions": "drwxr-xr-x"
                },
                {
                    "name": "parser.go",
                    "size": 1622,
                    "time_modified": 1700202950,
                    "permissions": "-rw-r--r--"
                },
                {
                    "name": "go.mod",
                    "size": 533,
                    "time_modified": 1699958000,
                    "permissions": "drwxr-xr-x"
                }
            ]
        },
        {
            "name": "token",
            "size": 4096,
            "time_modified": 1699954070,
            "permissions": "drwxr-xr-x",
            "contents": [
                {
                    "name": "token.go",
                    "size": 910,
                    "time_modified": 1699954070,
                    "permissions": "-rw-r--r--"
                },
                {
                    "name": "go.mod",
                    "size": 66,
                    "time_modified": 1699944730,
                    "permissions": "drwxr-xr-x"
                }
            ]
        }
    ]
}

long_listing_result = """-rw-r--r-- 1071 Nov 14 06:57 LICENSE
-rw-r--r--   83 Nov 14 06:57 README.md
drwxr-xr-x 4096 Nov 14 11:28 ast
-rw-r--r--   60 Nov 14 09:21 go.mod
drwxr-xr-x 4096 Nov 14 10:51 lexer
-rw-r--r--   74 Nov 14 09:27 main.go
drwxr-xr-x 4096 Nov 17 08:21 parser
drwxr-xr-x 4096 Nov 14 10:27 token\n"""

long_listing_result_all = """-rw-r--r-- 8911 Nov 14 06:57 .gitignore
-rw-r--r-- 1071 Nov 14 06:57 LICENSE
-rw-r--r--   83 Nov 14 06:57 README.md
drwxr-xr-x 4096 Nov 14 11:28 ast
-rw-r--r--   60 Nov 14 09:21 go.mod
drwxr-xr-x 4096 Nov 14 10:51 lexer
-rw-r--r--   74 Nov 14 09:27 main.go
drwxr-xr-x 4096 Nov 17 08:21 parser
drwxr-xr-x 4096 Nov 14 10:27 token\n"""
