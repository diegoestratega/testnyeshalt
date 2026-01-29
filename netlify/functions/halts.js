const fetch = require('node-fetch');

exports.handler = async function(event, context) {
  const NYSE_URL = "https://www.nyse.com/api/trade-halts/current/download";

  try {
    const response = await fetch(NYSE_URL, {
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
      },
      timeout: 8000
    });

    if (!response.ok) {
      return { statusCode: response.status, body: `Error: ${response.statusText}` };
    }

    const data = await response.text();

    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Cache-Control": "public, s-maxage=60",
        "Content-Type": "text/plain; charset=utf-8"
      },
      body: data
    };
  } catch (error) {
    return { statusCode: 500, body: error.toString() };
  }
};
