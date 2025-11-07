# Card Game App

Full-stack multiplayer card game server with real-time gameplay, bots (AI and non-AI), and advanced analytics.

Built to be game‑agnostic so new games are easy to add.

Try it out: https://gm-card-games.up.railway.app/

## Features (WIP)

- **Real-time multiplayer** via WebSockets
- **Bot players** with different levels; ML-capable
- **Event‑sourced architecture** with event‑sourced game engines
- **Detailed statistics** and game analysis tools (planned)
- **Multiple card games** (starting with ‘Five Hundred’)

## Tech Stack

- **Backend**: Python, Django, Django REST Framework, Channels
- **Frontend**: TypeScript, React
- **DB**: PostgreSQL

## Project Status

🚧 Work in Progress — working on improving db models and game replays

## About Five Hundred

Five Hundred is a trick‑taking card game not well known globally and rarely available online. This project aims to make it accessible to players worldwide while showcasing modern software architecture patterns.

## Roadmap

- [x] Core game engine for Five Hundred
- [x] Simple bot players
- [x] Game‑agnostic backend architecture
- [x] REST API for managing users and interacting with game tables
- [x] Minimalistic React FE for easier interaction with the API
- [x] User‑friendly React frontend (mostly AI generated just for POC)
- [x] WebSocket server
- [ ] Replay/history API using shortliving snapshot caching and bg tasks
- [ ] Game statistics/analyzing
- [ ] ELO tracking
- [ ] Private tables/invites
- [ ] Better UI, clean up AI generated sphageti code
- [ ] Table Chat
- [ ] AI and smart algorithmic bot opponents
- [ ] More games