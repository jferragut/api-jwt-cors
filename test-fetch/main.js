let store = {
    access_token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDY1MDU2NTksIm5iZiI6MTYwNjUwNTY1OSwianRpIjoiMTQ5MTZjZjUtMDY2OS00ZTEzLWE3YzktYzVmNjhmYzQwNDk3IiwiZXhwIjoxNjA2NzY0ODU5LCJpZGVudGl0eSI6Imxyb2RyaWd1ZXpANGdlZWtzLmNvIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.gX0oV2Ae3auROyft4I4JXUGxa4HItfAjtdOM4wzdUu8",
}

const getProfile = () => {
    fetch("http://localhost:5000/api/profile", {
        "method": "GET",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + store.access_token
        }
    })
        .then(response => {
            console.log(response);
            return response.json()
        })
        .then(data => {
            console.log(data);
        })
        .catch(err => {
            console.error(err);
        });
}

getProfile();