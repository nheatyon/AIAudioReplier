## Install

To use the script via python <b>(>=3.11)</b>, you need to download the source and go to the folder where the "requirements.txt" file is located. Here you will need to execute the following command:
```sh
pip3 install -r requirements.txt
```

## Usage
Once the dependencies are installed, you will need to run the script to start the Flask web server.<br/>
```sh
python3 __main__.py
```
After starting it, you can send POST requests to the “answer-to-audio” endpoint, specifying a json containing the base64 obtained from your audio.

<mark><b>Note:</b> The script was made with the intent of working for the <a href="https://en.wikipedia.org/wiki/Nao_(robot)">NAO robot</a>, passing (through Flask) a base64 reference value equivalent to the “.ogg” audio recorded by it. Other types of audio files may be supported.</mark>

```sh
curl -X POST http://127.0.0.1/answer-to-audio -d '{ "data": "base64_encoded_audio_file" }'
```

## Contributing

Any contribution to the project is really <b>appreciated</b>. Feel free to fork the project and commit your changes!<br/>
