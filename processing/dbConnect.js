const mysql = require('mysql2/promise');
const { MongoClient } = require("mongodb");

const sqlConnection = mysql.createPool({
    host: process.env.MYSQL_HOST,
    user: process.env.MYSQL_ROOT_USERNAME,
    password: process.env.MYSQL_ROOT_PASSWORD,
    database: process.env.MYSQL_DATABASE,
    port: process.env.MYSQL_PORT,
    waitForConnections: true,
    connectionLimit: 10,
    maxIdle: 10,
    idleTimeout: 60000,
    queueLimit: 0
});

const mongoUser = process.env.MONGO_INITDB_ROOT_USERNAME;
const mongoPass = process.env.MONGO_INITDB_ROOT_PASSWORD;
const mongoHost = process.env.MONGO_HOST;
const mongoPort = process.env.MONGO_PORT;

const mongoURI = `mongodb://${mongoUser}:${mongoPass}@${mongoHost}:${mongoPort}`;

const mongoClient = new MongoClient(mongoURI);

exports.sqlConnection = sqlConnection;
exports.client = mongoClient;