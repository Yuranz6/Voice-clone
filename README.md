# Voice Clone Chat

A web application that lets you clone voices and have AI conversations using those cloned voices. Uses ElevenLabs for voice cloning and Google Gemini for AI chat.

## What It Does

- Upload audio files to clone voices
- Chat with an AI assistant
- AI responses are spoken using your cloned voice

## Setup

1. Install dependencies:

   ```bash
   npm run install-all
   ```

2. Create a `.env` file in the root directory:

   ```
   ELEVENLABS_API_KEY=your_key_here
   GOOGLE_AI_API_KEY=your_key_here
   PORT=3001
   NODE_ENV=development
   CLIENT_URL=http://localhost:3000
   ```

3. Start the app:

   ```bash
   npm run dev
   ```

   Backend runs on http://localhost:3001
   Frontend runs on http://localhost:3000

## Usage

1. Upload an audio file (MP3, WAV, etc.) to clone a voice
2. Select the cloned voice from the list
3. Type a message and send
4. The AI responds with text and audio using your cloned voice

## Tech Stack

- Backend: Node.js, Express
- Frontend: React
- APIs: ElevenLabs (voice), Google Gemini (chat)

## Documentation

- [SETUP.md](./SETUP.md) - Detailed setup instructions
- [API_KEYS.md](./API_KEYS.md) - How to get API keys
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment guide
- [PRICING.md](./PRICING.md) - Cost information

## License

MIT
