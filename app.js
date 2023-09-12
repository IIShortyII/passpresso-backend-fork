const express = require('express')
var db = require("./database.js")
const app = express()
const PORT = 3000
var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.send('PasspressoSecure server is running!')
})

app.listen(PORT, () => {
    console.log(`Example app listening on port ${PORT}`)
})

app.get("/api/users", (req, res, next) => {
    const sql = "select * from user";
    db.all(sql, [], (err, rows) => {
        if (err) {
            res.status(400).json({"error": err.message});
            return;
        }
        res.json({
            "message": "success",
            "data": rows
        })
    });
});

app.get("/api/passwords", (req, res, next) => {
    const sql = "select * from password";
    db.all(sql, [], (err, rows) => {
        if (err) {
            res.status(400).json({"error": err.message});
            return;
        }
        res.json({
            "message": "success",
            "data": rows
        })
    });
});

app.get("/api/user/:uId/password", (req, res, next) => {
    const passwordsQuery = "select serviceUrl, username from password WHERE uId = ?"
    db.all(passwordsQuery, req.params.uId, (err, passwordRows) => {
        if (err) {
            res.status(400).json({"error": err.message});
            return;
        }
        const numberOfPasswords = passwordRows.length;
        const randomPassword = numberOfPasswords === 0 ? {} : passwordRows[Math.floor(Math.random() * numberOfPasswords)];


        const userScoreQuery = "select score from user WHERE uId = ?"
        db.all(userScoreQuery, req.params.uId, (err, scoreRows) => {
            if (err) {
                res.status(400).json({"error": err.message});
                return;
            }
            if (scoreRows.length === 0) {
                res.status(400).json({"error": "User doesn't exists"});
                return;
            }
            const responseWithScore = {score: scoreRows[0].score, password: randomPassword};
            res.json({
                "message": "success",
                "data": responseWithScore
            })
        });
    });
});

app.post("/api/passwords/add", (req, res, next) => {
    const passwords = req.body.passwords;
    const uId = req.body.uId;
    const score = req.body.score;
    const errors = [];

    if (!uId) {
        errors.push("No uId specified");
    }
    if (!score) {
        errors.push("No score specified");
    }
    if (!passwords) {
        errors.push("No passwords specified");
    }
    if (errors.length) {
        res.status(400).json({"error": errors.join(",")});
        return;
    }

    const findUserQuery = "select * from user WHERE uId = ?"
    db.all(findUserQuery, uId, (err, rows) => {
        if (err) {
            res.status(400).json({"error": err.message});
            return;
        }


        if (rows.length === 0) {
            //add user if not exists
            const insertUserQuery = 'INSERT INTO user (uId, score) VALUES (?, ?)'
            db.run(insertUserQuery, [uId, score])
            console.log("Inserted user")
        } else {
            //update score if user exists
            const updateUserQuery = 'UPDATE user SET score = ? WHERE uId = ?'
            db.run(updateUserQuery, [score, uId])
            console.log("Updated score")

            //delete all passwords if user exists
            const deleteAllPasswordsQuery = 'DELETE FROM password WHERE uId = ?'
            db.run(deleteAllPasswordsQuery, [uId])
        }

        //add passwords
        passwords.forEach(password => {
            const insertPasswordQuery = 'INSERT INTO password (uId, serviceUrl, username) VALUES (?, ?, ?)'
            db.run(insertPasswordQuery, [uId, password.serviceUrl, password.username])
            console.log("Inserted password")
        })
    })

    res.json({
        "message": "success"
    })
})
