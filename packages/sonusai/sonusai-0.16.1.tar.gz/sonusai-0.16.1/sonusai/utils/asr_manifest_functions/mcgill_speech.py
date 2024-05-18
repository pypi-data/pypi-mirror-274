from sonusai.utils.asr_manifest_functions import PathInfo


def get_mcgill_speech_manifest_entry(entry: PathInfo, transcript_data: list[str]) -> dict:
    from os.path import splitext
    from os.path import basename
    from subprocess import check_output

    from sonusai import SonusAIError

    name = splitext(entry.abs_path)[0]
    duration = float(check_output(f'soxi -D {entry.abs_path}', shell=True))
    # i.e., from MA01_02.wav, get 01_02
    promptname = basename(name)[2:]
    # paragraph num
    pnum = int(promptname[0:2])
    snum = int(promptname[3:5])
    idx = 11 * (pnum - 1) + (snum - 1)
    try:
        # remove prompt-id prefix and \n suffix
        text = transcript_data[idx][6:-1]
    except IndexError:
        raise SonusAIError(f'Could not find {promptname}, idx {idx} in transcript data')

    return {
        'audio_filepath': entry.audio_filepath,
        'text':           text,
        'duration':       duration,
    }
