const express = require('express')
const app = express()
const port = 3000

const API_KEY = require('./key.js').API_KEY


async function getWeather() {
    const api_call = `http://api.openweathermap.org/data/2.5/weather?q=Singapore&appid=${API_KEY}`;
    const response = await fetch(api_call);

    const data = await response.json()
    const temperature = data.main.temp / 10;
    return temperature;
}

app.get('/', async(req, res) => {
    temperature = await getWeather();
    res.send(`The temperature in Singapore is ${temperature} degrees celsius`);
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
})