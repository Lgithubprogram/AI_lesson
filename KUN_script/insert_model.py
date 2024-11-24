from pathlib import Path
import os
import scipy.io.wavfile as wavf
import torch
from utils import get_hparams_from_file, load_checkpoint
from torch import no_grad, LongTensor

from commons import intersperse
from models import SynthesizerTrn
from text import text_to_sequence
import pyaudio

device = "cuda:0" if torch.cuda.is_available() else "cpu"
#我只训练了CJ模型
language_marks = {
    "JP": "[JA]",
    "ZH": "[ZH]",
    "EN": "[EN]",
    "Mix": ""
}


def get_text(text, hps, is_symbol):
    text_norm = text_to_sequence(text, hps.symbols, [] if is_symbol else hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm


def generate(model_path = "model", text = None, noise_scale=.667, noise_scale_w=.6, length=.8, language="Mix"):
    """
    :param text: Text to generate
    :param noise_scale: THE EMOTION
    :param noise_scale_w: phoneme scale
    :param length: overall talk speed
    :param language: The language, can be ["Mix", "JP", "CH", "EN"]
    """
    model_config_path = os.path.join(model_path, "config.json")
    print("Model config path:", model_config_path)  # 打印模型配置路径，确保正确
    # output_dir = Path("output/")
    # output_dir.mkdir(parents=True, exist_ok=True)
    output_dir = os.path.join(model_path, "output")

    hps = get_hparams_from_file(model_config_path)
    print("Loaded hps:", hps)  # 打印出hps对象的内容
    print("hps symbols:", getattr(hps, 'symbols', 'symbols not found'))

    net_g = SynthesizerTrn(
        len(hps.symbols),
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers=hps.data.n_speakers,
        **hps.model).to(device)
    _ = net_g.eval()
    checkpoint_path = os.path.join(model_path, "G_latest.pth")
    _ = load_checkpoint(checkpoint_path=checkpoint_path, model=net_g, optimizer=None,drop_speaker_emb=False)

    speaker_ids = hps.speakers

    if language is not None:
        text = language_marks[language] + text + language_marks[language]
        #这里我们指定说话人
        speaker_id = speaker_ids["Kun"]
        stn_tst = get_text(text, hps, False)
        with no_grad():
            x_tst = stn_tst.unsqueeze(0).to(device)
            x_tst_lengths = LongTensor([stn_tst.size(0)]).to(device)
            sid = LongTensor([speaker_id]).to(device)
            audio = net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale, noise_scale_w=noise_scale_w,
                                length_scale=1.0 / length)[0][0, 0].data.cpu().float().numpy()
        del stn_tst, x_tst, x_tst_lengths, sid

        wavf.write(str(output_dir) + "/output.wav", hps.data.sampling_rate, audio)
        #这是不保存的代码
        #直接播放音频
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=hps.data.sampling_rate,
                        output=True)
        stream.write(audio, len(audio))
        stream.stop_stream()
        stream.close()
        p.terminate()

    return str(output_dir) + "/output.wav"


if __name__ == "__main__":
    generate(text = "全民制作人大家好，我是蔡徐坤", language="ZH")