# Lofied - Spotify Playlist to Lo-fi Converter

## Overview
Lofied is a Python-based application that allows users to convert their Spotify playlists into lo-fi versions. The application downloads songs from Spotify playlists, processes them through a music separation pipeline, and creates lo-fi versions of the tracks. It can also convert songs into sheet music format for musical analysis and learning.

## Features
- Create and manage Spotify playlists
- Download songs from Spotify playlists
- Convert songs to lo-fi versions
- Convert songs to sheet music format
- Edit and update existing playlists
- Sync playlists with Spotify

## Technical Stack
- **Programming Language**: Python 3.x
- **Key Libraries and Tools**:
  - spotdl: For downloading Spotify tracks
  - torchaudio music separation pipeline
  - Pedal Board (Spotify) audio transformation
  - Basic Pitch: For sheet music conversion
  - MySQL: For database management
  - Virtual Environment (venv) for dependency management

## Project Structure
```
Lofied/
├── src/
│   ├── main.py           # Main application entry point
│   ├── playlist.py       # Playlist management functionality
│   ├── spotdl.py         # Spotify download integration
│   ├── mySQL.py          # Database operations
│   ├── setup.py          # Environment setup
│   └── pipelines/
│       ├── musicSeperation.py  # Music processing pipeline
│       ├── audioTransformation.py  # Audio transformations
│       └── convertToSheet.py   # Sheet music conversion
├── playlists/            # Storage for downloaded and processed playlists
│   └── [playlist_name]/
│       ├── notlofied/    # Original downloaded tracks
│       ├── lofied/       # Processed lo-fi versions
│       └── sheets/       # Generated sheet music files
└── venv/                 # Python virtual environment
```

## Installation and Setup
1. Clone the repository
2. Navigate to the project directory
3. Create playlist folder in root of project
4. Run the application:
   ```bash
   docker compose up --build -d
   docker run -it -v "$(pwd)/playlists:/app/playlists" jam-hacks-2025-server
   ```
   The setup script will automatically:

## Usage
The application provides a menu-driven interface with the following options:
1. Create new playlist
2. Sync existing playlist
3. Delete playlist
4. Download playlist
5. Convert playlist to lo-fi
6. Convert to music sheet

### Creating a New Playlist
1. Select option 1 from the main menu
2. Enter a name for your playlist
3. Input Spotify URLs for the songs (enter 'x' when finished)
4. The application will download the songs and prepare them for processing

### Converting to Lo-fi
1. Select option 5 from the main menu
2. Enter the name of the playlist to convert
3. The application will process each song through the music separation pipeline
4. Converted lo-fi versions will be stored in the playlist's 'lofied' directory

### Converting to Sheet Music
1. Select option 6 from the main menu
2. Enter the name of the playlist to convert
3. The application will:
   - Separate vocals and other instruments
   - Merge them with optimal balance
   - Convert the audio to MIDI format
   - Save the sheet music in the playlist's 'sheets' directory

## Development Process
The project was developed in several phases:
1. Initial setup and environment configuration
2. Spotify integration using spotdl
3. Implementation of playlist management features
4. Development of the music separation pipeline
5. Integration of all components
6. Testing and refinement
7. Addition of sheet music conversion feature
8. Optimization of audio processing pipeline

## Challenges and Solutions
1. **Music Processing Pipeline**
   - Challenge: Implementing efficient music separation
   - Solution: Developed a custom pipeline using advanced audio processing techniques
   - Recent Improvement: Optimized pipeline to process audio in memory without intermediate file storage

2. **Spotify Integration**
   - Challenge: Handling various Spotify URL formats and track metadata
   - Solution: Utilized spotdl library with custom wrappers for better control

3. **File Management**
   - Challenge: Organizing downloaded and processed files
   - Solution: Implemented a structured directory system with clear separation between original and processed tracks

4. **Persistent Docker Data Storage**
   - Challenge: Playlists created in container needs to sync with host data
   - Solution: Implemented bind mounts (shared volume)
   - Need to run `docker run -it -v "$(pwd)/playlists:/app/playlists" lofied-server` where `$(pwd)/playlists` is the host directory and `/app/playlists` is the contianer directory and `-v` binds them together

5. **Sheet Music Conversion**
   - Challenge: Accurate conversion of audio to sheet music
   - Solution: Implemented a two-step process using music separation and Basic Pitch
   - Recent Improvement: Optimized audio processing to maintain quality while reducing file operations

## Learning Outcomes
- Advanced audio processing techniques
- Spotify API integration
- Python project structure and organization
- Virtual environment management
- File system operations in Python
- Command-line interface design
- Music theory and sheet music generation
- Audio-to-MIDI conversion techniques

## Future Improvements
- Add support for more music platforms
- Implement batch processing for large playlists
- Add user authentication
- Create a web interface
- Add more audio processing options
- Implement progress tracking for long operations
- Add support for different sheet music formats
- Implement real-time audio processing
- Add support for custom audio effects
- Develop a mobile application 