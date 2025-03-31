![Logo of the project](data/logo.png)

# The Signoffagen

Script for isolating singoffs from streamer *ThePrimagen* YouTube: [ThePrimagen](https://www.youtube.com/@ThePrimeTimeagen), GitHub: [ThePrimagen](https://github.com/theprimeagen). This was just a silly project that I used to practice my Python skills and methods of text parsing. Please bare with me as I'm not an actual software developer, just a datascientist with time to spare. There will be plenty of bad practices to be seen in this repo.

## Installing / Getting started

Pull the repo. Then use `pip install -r requirements.txt` to install dependencies.

Alternativley, you can simply open the script in your IDE of choice and install any missing libraries.

NOTE: You may need to create some required directories as I can't get git to keep empty directories in the project.

Once isntalled, open Primeagen's video library found here: https://www.youtube.com/@ThePrimeTimeagen/videos. scroll to the bottom (holding down the End key helps) until videos stop loading.

Open the browser dev tools and copy the HTML element that contains all the video thumbnails, links and titles. Paste these into `export.html`.

Then run `__main__.py` and follow the prompts in the terminal.

## Design and Logic

The script has 4 distinct stages:

### (1) Extract Video Links from HTML Blob
This stage will extract all vide titles and href's from the html blob in `export.html` which was copied from The Primeagens youtube channel.

### (2) Harvest Transcripts
This stage will iterate through each video in the library and pull the captions from YouTube's API.

### (3) Measure Time Against Characters
This stage will iterate through video captions file and add:
1. each captions length in characters.
1. each captions position from the start of the video in characters.

### (4) Consolidate to Dataset
This stage will then parse through the transcripts and find delimiters to isolate the signoff.


## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are welcomed.

## Links

- ThePrimeagen on YouTube: https://www.youtube.com/@ThePrimeTimeagen
- ThePrimeagen on GitHub: https://github.com/theprimeagen
- Repository: https://github.com/sc00pp/signoffagen
- jdepoix's YouTube Transcript API tool: https://github.com/jdepoix/youtube-transcript-api


## Licensing

The code in this project is licensed under MIT license.