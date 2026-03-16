# AutoTranscribe - Batch Audio & Video Transcription

Standalone transcription tool powered by OpenAI Whisper. Batch process multiple audio/video files with customizable output formats.

## Features

- **Batch Processing** - Upload and transcribe multiple files at once
- **Model Selection** - Choose from 5 Whisper models (Tiny to Large) for speed vs accuracy
- **Multiple Export Formats** - Plain text (.txt), Word documents (.docx), and SRT subtitles (.srt)
- **Language Support** - 99 languages with auto-detection or manual selection
- **Timestamp Options** - Include timestamps in transcripts for reference
- **Translation** - Transcribe foreign language audio and translate to English
- **Progress Tracking** - Visual progress bar and per-file status
- **Download Management** - Download individual files or all at once

## Quick Start

1. **Double-click `start_autotranscribe.bat`**
2. **Upload audio/video files** (drag & drop or click to browse)
3. **Choose settings** (model, language, output formats)
4. **Click "Start Transcription"**
5. **Download your transcripts** when complete

## Requirements

- Python 3.8+
- FFmpeg (for processing audio/video files)
- Required Python packages:
  - flask
  - flask-cors
  - openai-whisper
  - python-docx

## Installation

### If You Already Have AutoClapper Set Up:

You already have all the dependencies! Just:
1. Copy the AutoTranscribe files to a new folder
2. Run `start_autotranscribe.bat`

### Fresh Installation:

1. **Install Python** (3.8 or newer) with pip
2. **Install FFmpeg** and add to system PATH
3. **Install Python packages:**
   ```
   pip install flask flask-cors openai-whisper python-docx
   ```
4. **Run AutoTranscribe:**
   ```
   start_autotranscribe.bat
   ```

See the main SETUP_GUIDE.md for detailed installation instructions.

## Whisper Models

Choose the right model for your needs:

| Model  | Speed    | Accuracy | RAM Usage | Best For                          |
|--------|----------|----------|-----------|-----------------------------------|
| Tiny   | Fastest  | Basic    | ~1GB      | Quick drafts, low-quality audio   |
| Base   | Fast     | Good     | ~1GB      | **Recommended for most uses**     |
| Small  | Medium   | Better   | ~2GB      | Higher accuracy needed            |
| Medium | Slow     | High     | ~5GB      | Professional transcription        |
| Large  | Slowest  | Best     | ~10GB     | Maximum accuracy, clean audio     |

**Note:** First time using each model will download it (39MB to 2.9GB).

## Supported File Formats

- **Audio:** MP3, WAV, M4A, FLAC, OGG, AAC
- **Video:** MP4, MOV, AVI, MKV, WMV, FLV

Whisper will automatically extract audio from video files.

## Output Formats

### Plain Text (.txt)
- Simple text file with the transcription
- Optional timestamps for each segment
- Easy to edit and share

### Word Document (.docx)
- Formatted document with title and metadata
- Optional timestamps in bold
- Professional appearance
- Ready for editing in Microsoft Word

### SRT Subtitles (.srt)
- Standard subtitle format
- Compatible with video players and editing software
- Includes precise timestamps for each line
- Can be imported into Premiere, Final Cut, DaVinci Resolve, etc.

## Usage Tips

### For Best Results:
- Use **Base model** for everyday work (good balance)
- Specify the **language** if you know it (improves accuracy)
- Use **timestamps** for long recordings you'll need to reference
- Enable **SRT output** if you plan to create subtitles

### For Speed:
- Use **Tiny model** for rough drafts
- Disable formats you don't need
- Process shorter clips rather than full-length videos

### For Accuracy:
- Use **Small or Medium model** for important work
- Ensure good audio quality (clear speech, minimal background noise)
- Specify the exact language rather than auto-detect
- Review and edit the output for critical content

## Workflow Examples

### Creating Subtitles for Video:
1. Upload your video file
2. Select language
3. Check "Subtitles (.srt)" output
4. Transcribe
5. Import .srt file into your video editor

### Transcribing Interviews:
1. Upload interview audio
2. Use "Base" or "Small" model
3. Check "Include timestamps"
4. Check "Word Document (.docx)"
5. Download and edit in Word

### Batch Processing Ad Scripts:
1. Upload all ad videos at once
2. Select "Base" model
3. Check "Plain Text (.txt)" and "Word Document (.docx)"
4. Let it process all files
5. Download all transcripts

## File Naming

Output files are automatically named:
```
[original_filename]_[timestamp].txt
[original_filename]_[timestamp].docx
[original_filename]_[timestamp].srt
```

Example: `MyAd_20250202_143022.txt`

All files are saved to the `transcriptions/` folder.

## Translation Feature

The "Translate to English" option will:
- Transcribe audio in any language
- Automatically translate to English
- Preserve timestamps

Note: Translation is slightly slower than regular transcription.

## Troubleshooting

### "FFmpeg is not installed"
- Install FFmpeg following the SETUP_GUIDE.md instructions
- Make sure FFmpeg is in your system PATH
- Restart Command Prompt after installation

### Transcription is very slow
- Use a smaller model (Tiny or Base)
- Check your CPU usage - close other programs
- Process shorter clips instead of full videos

### Low accuracy / lots of mistakes
- Use a larger model (Small or Medium)
- Improve audio quality if possible
- Specify the exact language
- Remove background noise from audio if possible

### Downloads not working
- Check the `transcriptions/` folder - files may already be there
- Make sure you have write permissions
- Try a different browser

### "Could not connect to backend"
- Make sure `start_autotranscribe.bat` is running
- The Command Prompt window must stay open
- Check that port 5001 is not blocked

## Comparing to AutoClapper

AutoTranscribe is a **standalone tool** separate from AutoClapper:

| Feature              | AutoClapper                   | AutoTranscribe                |
|----------------------|-------------------------------|-------------------------------|
| **Purpose**          | Script & clapper generation   | Audio transcription           |
| **Port**             | 5000                          | 5001                          |
| **Can run together** | Yes                           | Yes                           |
| **Transcription**    | Single file, auto-populates   | Batch files, multiple formats |

You can run both at the same time! They use different ports and don't interfere with each other.

## Advanced: Running Without Batch File

If you prefer to run manually:

```bash
cd C:\path\to\autotranscribe
python autotranscribe_app.py
```

Then open your browser to: `http://localhost:5001`

## Performance Notes

Processing time depends on:
- **Model size** - Larger = slower but more accurate
- **Audio length** - Longer = more time
- **CPU/GPU** - Faster hardware = faster processing
- **First run** - Model downloads only happen once

Rough estimates (Base model on modern PC):
- 1 minute of audio = 10-20 seconds processing
- 10 minutes of audio = 2-3 minutes processing
- 1 hour of audio = 10-15 minutes processing

## Storage

Models are downloaded once and stored in your user directory:
- Windows: `C:\Users\[YourName]\.cache\whisper\`

You don't need to re-download them for each use.

## Support

For issues or questions:
1. Check the SETUP_GUIDE.md for installation help
2. Verify FFmpeg is installed: `ffmpeg -version`
3. Verify Whisper is installed: `python -c "import whisper; print('OK')"`
4. Check the Command Prompt window for error messages

## Credits

- Powered by OpenAI Whisper - https://github.com/openai/whisper
- Built for video production workflows
- Part of the AutoClapper suite of tools
