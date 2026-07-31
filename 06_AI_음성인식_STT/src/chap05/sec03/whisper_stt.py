import os

import pandas as pd
import torch
from dotenv import load_dotenv
from pyannote.audio import Pipeline
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


load_dotenv()

ffmpeg_bin = os.getenv("FFMPEG_BIN")
if ffmpeg_bin:
    os.environ["PATH"] += os.pathsep + ffmpeg_bin


def whisper_stt(
    audio_file_path: str,
    output_file_path: str = "./output.csv",
):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = "openai/whisper-large-v3-turbo"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True,
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
        return_timestamps=True,
        chunk_length_s=10,
        stride_length_s=2,
    )

    result = pipe(audio_file_path)
    df = whisper_to_dataframe(result, output_file_path)

    return result, df


def whisper_to_dataframe(result, output_file_path):
    start_end_text = []

    for chunk in result["chunks"]:
        start = chunk["timestamp"][0]
        end = chunk["timestamp"][1]
        text = chunk["text"].strip()
        start_end_text.append([start, end, text])
        df = pd.DataFrame(start_end_text, columns=["start", "end", "text"])
        df.to_csv(output_file_path, index=False, sep="|")

    return df


def speaker_diarization(
    audio_file_path: str,
    output_rttm_file_path: str,
    output_csv_file_path: str,
):
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise RuntimeError("HF_TOKEN 환경변수를 설정해 주세요.")

    diarization_model = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token,
    )

    if torch.cuda.is_available():
        diarization_model.to(torch.device("cuda"))
        print("cuda is available")
    else:
        print("cuda is not available")
    diarization_pipeline = diarization_model(audio_file_path)

    with open(output_rttm_file_path, "w", encoding="utf-8") as rttm:
        diarization_pipeline.write_rttm(rttm)

    df_rttm = pd.read_csv(
        output_rttm_file_path,
        sep=" ",
        header=None,
        names=[
            "type",
            "file",
            "chnl",
            "start",
            "duration",
            "C1",
            "C2",
            "speaker_id",
            "C3",
            "C4",
        ],
    )

    df_rttm["end"] = df_rttm["start"] + df_rttm["duration"]
    df_rttm["number"] = None
    df_rttm.at[0, "number"] = 0

    for i in range(1, len(df_rttm)):
        if df_rttm.at[i, "speaker_id"] != df_rttm.at[i - 1, "speaker_id"]:
            df_rttm.at[i, "number"] = df_rttm.at[i - 1, "number"] + 1
        else:
            df_rttm.at[i, "number"] = df_rttm.at[i - 1, "number"]

    df_rttm_grouped = df_rttm.groupby("number").agg(
        start=pd.NamedAgg(column="start", aggfunc="min"),
        end=pd.NamedAgg(column="end", aggfunc="max"),
        speaker_id=pd.NamedAgg(column="speaker_id", aggfunc="first"),
    )
    df_rttm_grouped["duration"] = (
        df_rttm_grouped["end"] - df_rttm_grouped["start"]
    )
    df_rttm_grouped.to_csv(output_csv_file_path, index=False, encoding="utf-8")

    return df_rttm_grouped


def stt_to_rttm(
    audio_file_path: str,
    stt_output_file_path: str,
    rttm_file_path: str,
    rttm_csv_file_path: str,
    final_output_csv_file_path: str,
):
    _, df_stt = whisper_stt(audio_file_path, stt_output_file_path)
    df_rttm = speaker_diarization(
        audio_file_path,
        rttm_file_path,
        rttm_csv_file_path,
    )
    df_rttm["text"] = ""

    for _, row_stt in df_stt.iterrows():
        overlap_dict = {}
        for i_rttm, row_rttm in df_rttm.iterrows():
            overlap = max(
                0,
                min(row_stt["end"], row_rttm["end"])
                - max(row_stt["start"], row_rttm["start"]),
            )
            overlap_dict[i_rttm] = overlap

        max_overlap = max(overlap_dict.values())
        max_overlap_idx = max(overlap_dict, key=overlap_dict.get)

        if max_overlap > 0:
            df_rttm.at[max_overlap_idx, "text"] += row_stt["text"] + "\n"

    df_rttm.to_csv(
        final_output_csv_file_path,
        index=False,
        sep="|",
        encoding="utf-8",
    )
    return df_rttm


if __name__ == "__main__":
    audio_file_path = "./chap05/audio/싼기타_비싼기타.mp3"
    stt_output_file_path = "./chap05/audio/싼기타_비싼기타.csv"
    rttm_file_path = "./chap05/audio/싼기타_비싼기타.rttm"
    rttm_csv_file_path = "./chap05/audio/싼기타_비싼기타_rttm.csv"
    final_csv_file_path = "./chap05/audio/싼기타_비싼기타_final.csv"

    df_rttm = stt_to_rttm(
        audio_file_path,
        stt_output_file_path,
        rttm_file_path,
        rttm_csv_file_path,
        final_csv_file_path,
    )
    print(df_rttm)
