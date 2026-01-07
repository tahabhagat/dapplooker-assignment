# Dapplooker Assignment

This is a FastAPI application that provides 2 APIs, one for retrieving crypto sentiment analysis using CoinGecko and Gemini API, and another for retrieving a wallet's pnl using Hyperliquid API.


## Utilisation
- Retrieve the CoinGecko API key from CoinGecko (Guide [here](https://docs.coingecko.com/docs/setting-up-your-api-key))
- Retrieve the Gemini API key from Google AI Studio  (Guide [here](https://ai.google.dev/gemini-api/docs/api-key#:~:text=Go%20to%20Google%20AI%20Studio.))
- 
- Set environment variables in the docker compose file
- Start the application using the docker compose file
```bash
# docker compose up -d
```
Alternatively, use podman
```bash
$ podman compose up -d
```

Access Swagger UI at ```http://localhost:8000/docs```, and test the 2 APIs
View the application logs using the 'logs' command
```bash
# docker compose logs -f dapplooker-assignment
```
OR
```bash
$ podman logs -f dapplooker-assignment
```

##TODO
- Use market chart resource for token sentiment analysis
- Add test cases using pytest.
- Create a github actions pipeline to build the docker image, and push to a container registry/deploy to a cloud platform
- Create custom exceptions for errors from downstream APIs and propogate correctly to frontend
- Create postman collection for testing the APIs
- Have tested with podman, test with docker as well to catch any issues
