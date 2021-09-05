# OptiHealth

Application developed for MedHack 2021 (just the backend).
The app generates meal plans for cancer patients by using convex optimization.

Example of a generated daily meal plan:

```json
[
    {
        "name": "Mic dejun",
        "foods": [
            {
                "name": "Iaurt",
                "quantity": 113,
                "calories": 70
            },
            {
                "name": "Fulgi de ovăz",
                "quantity": 113,
                "calories": 398
            }
        ]
    },
    {
        "name": "Gustare",
        "foods": [
            {
                "name": "Afine",
                "quantity": 107,
                "calories": 68
            },
            {
                "name": "Iaurt",
                "quantity": 163,
                "calories": 100
            }
        ]
    },
    {
        "name": "Prânz",
        "foods": [
            {
                "name": "Somon",
                "quantity": 152,
                "calories": 313
            },
            {
                "name": "Fasole",
                "quantity": 99,
                "calories": 259
            },
            {
                "name": "Legume mexicane fierte",
                "quantity": 108,
                "calories": 83
            }
        ]
    },
    {
        "name": "Gustare",
        "foods": [
            {
                "name": "Afine",
                "quantity": 107,
                "calories": 68
            },
            {
                "name": "Iaurt",
                "quantity": 163,
                "calories": 100
            }
        ]
    },
    {
        "name": "Cină",
        "foods": [
            {
                "name": "Supă cremă de linte",
                "quantity": 115,
                "calories": 374
            }
        ]
    }
]
```
