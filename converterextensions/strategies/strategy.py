import pypandoc
import subprocess

from PIL import Image
from json import load
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from pydub import AudioSegment
from moviepy.editor import *
from json import dump
from xmltodict import parse


class AbstractStrategy:
    def convert(self, source, target):
        raise NotImplementedError


class DocxToPdfStrategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        out_dir = ['/'.join(target.split('/')[:-1])]
        cmd = 'libreoffice --convert-to pdf --outdir'.split() + out_dir + [source]
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        p.wait(timeout=10)
        stdout, stderr = p.communicate()
        if stderr:
            raise subprocess.SubprocessError(stderr)
        os.rename(source.replace('.docx', '.pdf'), target)


class DocxToTxtStrategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        pypandoc.convert_file(source, 'plain', outputfile=target)


class JpgToPngStrategy(AbstractStrategy):
    def convert(self, source, target):
        image = Image.open(source)
        image.save(target)


class JsonToXmlStrategy(AbstractStrategy):
    def convert(self, source, target):
        xml = ''
        with open(source, 'r') as source_file:
            xml = dicttoxml(load(source_file), attr_type=False)
        xml_dom = parseString(xml)
        with open(target, 'w') as target_file:
            target_file.write(xml_dom.toprettyxml())


class Mp3ToRawStrategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        mp3_audio = AudioSegment.from_mp3(source)
        mp3_audio.export(target, format='raw')


class Mp3ToWavStrategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        mp3_audio = AudioSegment.from_mp3(source)
        mp3_audio.export(target, format='wav')


class Mp4ToMp3Strategy(AbstractStrategy):
    def convert(self, source, target):
        video = VideoFileClip(source)
        video.audio.write_audiofile(target)
        video.close()


class PngToJpgStrategy(AbstractStrategy):
    def convert(self, source, target):
        image = Image.open(source)
        rgb_image = image.convert('RGB')
        rgb_image.save(target)


class RawToMp3Strategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        raw_audio = AudioSegment.from_file(file=source, frame_rate=44100, channels=2, sample_width=2)
        raw_audio.export(target, format='mp3')


class RawToWavStrategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        mp3_audio = AudioSegment.from_file(file=source, frame_rate=44100, channels=2, sample_width=2)
        mp3_audio.export(target, format='wav')


class WavToMp3Strategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        wav_audio = AudioSegment.from_wav(source)
        wav_audio.export(target, format='mp3')


class WavToRawStrategy(AbstractStrategy):
    def convert(self, source: str, target: str):
        wav_audio = AudioSegment.from_wav(source)
        wav_audio.export(target, format='raw')


class XmlToJsonStrategy(AbstractStrategy):
    def convert(self, source, target):
        dict_data = ''
        with open(source, 'r') as source_file:
            dict_data = parse(source_file.read())
        with open(target, "w") as target_file:
            dump(dict_data, target_file, indent=4)


class ImagesToPdfStrategy(AbstractStrategy):
    def convert(self, source, target):
        images = []
        for image_source in source:
            image = Image.open(image_source)
            images.append(image.convert('RGB'))
        images[0].save(target, save_all=True, append_images=images[1:])
