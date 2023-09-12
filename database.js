const sqlite3 = require('sqlite3').verbose()
const DB_SOURCE = "db.sqlite"

const USERS_MOCK_DATA = [
    ["CBCB3C50", 77],
    ["A4A29E5B", 100],
    ["CB868650", 32],
    ["8BFF4F50", 77],
    ["742B695B", 98]
]
const PASSWORD_MOCK_DATA = [
    ["CBCB3C50", "https://uni2work.ifi.lmu.de/", "mustermann.dennis@campus.lmu.de"],
    ["CB868650", "https://www.amazon.de/", "raffael@example.com"],
    ["8BFF4F50", "https://www.facebook.com/", "jonas@exampl.com"],
    ["742B695B", "https://www.google.com/", "sebastian@example.com"]
]

const db = new sqlite3.Database(DB_SOURCE, (err) => {
    if (err) {
        // Cannot open database
        console.error(err.message)
        throw err
    } else {
        console.log('Connected to the SQLite database.')
        db.run(`CREATE TABLE user
                (
                    uId   text PRIMARY KEY,
                    score INTEGER
                );
            `,
            (err) => {
                if (err) {
                    // Table already created
                } else {
                    const insertUserQuery = 'INSERT INTO user (uId, score) VALUES (?, ?)'

                    USERS_MOCK_DATA.forEach((user) => {
                        db.run(insertUserQuery, user)
                        console.log(`Inserted user ${user[0]} with score ${user[1]} into database`)
                    })

                }
            });

        db.run(`CREATE TABLE password
                (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    uId        text,
                    serviceUrl text,
                    username   text,
                    FOREIGN KEY (uId) REFERENCES user (uId)
                );
            `,
            (err) => {
                if (err) {
                    // Table already created
                } else {
                    const insertPasswordQuery = "INSERT INTO password (uId, serviceUrl, username) VALUES (?, ?, ?)"
                    PASSWORD_MOCK_DATA.forEach((password) => {
                        db.run(insertPasswordQuery, password)
                        console.log(`Inserted password for user ${password[0]} with serviceUrl ${password[1]} and username ${password[2]} into database`)
                    })
                }
            });
        console.log("\n----------------------------------")
        console.log("🚀 Server started successfully")
        console.log("💻 Visit http://localhost:3000/api/users to see all users")
        console.log("💻 Visit http://localhost:3000/api/passwords to see all passwords")
    }
});


module.exports = db
